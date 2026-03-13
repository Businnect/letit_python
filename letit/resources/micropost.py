from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from requests_toolbelt.multipart.encoder import MultipartEncoder

# import sys
# import os
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from letit.schemas.micropost import PostType
from letit.schemas.common import CreatedWithPublicIdAndLinkResponse

if TYPE_CHECKING:
    from ..client import LetIt

class MicropostResource:
    def __init__(self, client: "LetIt"):
        self._client = client

    def client_create_micropost(
        self,
        body: str,
        title: Optional[str] = None,
        post_type: PostType = PostType.TEXT,
        community_name: Optional[str] = None,
        parent_micropost_public_id: Optional[str] = None,
        parent_micropost_comment_public_id: Optional[str] = None,
        allow_comments: bool = True,
        is_draft: bool = False,
        file: Optional[tuple] = None,  # ("filename.png", open(..., "rb"), "image/png")
    ) -> CreatedWithPublicIdAndLinkResponse:
        """
        A client creates a micropost.

        Args:
            body: The content of the post.
            title: Required for original posts.
            post_type: "TEXT" or "MEDIA". Defaults to "TEXT".
            community_name: Optional community to post in.
            parent_micropost_public_id: For replies.
            parent_micropost_comment_public_id: For nested replies.
            allow_comments: Whether comments are allowed. Defaults to True.
            is_draft: Save as draft. Defaults to False.
            file: Tuple of (filename, file_object, mime_type) for MEDIA posts.

        Returns:
            MicropostResponse with public_id and link.

        Example:
            # Text post
            post = client.micropost.create(title="Hello", body="World")

            # Media post
            with open("photo.png", "rb") as f:
                post = client.micropost.create(
                    title="My photo",
                    body="Check this out",
                    post_type="MEDIA",
                    file=("photo.png", f, "image/png"),
                )
        """

        fields = {
            "body": body,
            "post_type": post_type,
            "allow_comments": str(allow_comments).lower(),
            "is_draft": str(is_draft).lower(),
        }

        if title:
            fields["title"] = title
        if community_name:
            fields["community_name"] = community_name
        if parent_micropost_public_id:
            fields["parent_micropost_public_id"] = parent_micropost_public_id
        if parent_micropost_comment_public_id:
            fields["parent_micropost_comment_public_id"] = parent_micropost_comment_public_id
        if file:
            fields["file"] = file  # tuple: ("filename.png", open(...), "image/png")

        m = MultipartEncoder(fields=fields)

        response = self._client._request(
            "POST",
            "/api/v1/client/micropost",
            data=m,
            headers={"Content-Type": m.content_type},
        )

        return CreatedWithPublicIdAndLinkResponse(**response.json())