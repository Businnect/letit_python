from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from requests_toolbelt.multipart.encoder import MultipartEncoder

from letit.schemas.micropost import PostType
from letit.schemas.common import CreatedWithPublicIdAndLinkResponse, VoteResponse

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
        file: Optional[tuple] = None,
    ) -> CreatedWithPublicIdAndLinkResponse:
        """
        Cria um micropost (texto, mídia ou reply).

        Args:
            body: Conteúdo do post.
            title: Obrigatório para posts originais.
            post_type: "TEXT" ou "MEDIA". Padrão: TEXT.
            community_name: Comunidade onde postar (opcional).
            parent_micropost_public_id: Para replies a um post.
            parent_micropost_comment_public_id: Para replies aninhados.
            allow_comments: Se permite comentários. Padrão: True.
            is_draft: Salvar como rascunho. Padrão: False.
            file: Tuple (filename, file_object, mime_type) para posts MEDIA.

        Returns:
            CreatedWithPublicIdAndLinkResponse com public_id e link.
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
            fields["file"] = file

        m = MultipartEncoder(fields=fields)

        response = self._client._request(
            "POST",
            "/api/v1/client/micropost",
            data=m,
            headers={"Content-Type": m.content_type},
        )

        return CreatedWithPublicIdAndLinkResponse(**response.json())

    def client_delete_micropost(self, public_id: str) -> None:
        """
        Deleta um micropost pelo public_id.

        Args:
            public_id: ID público do post a ser deletado.

        Returns:
            None (204 No Content em caso de sucesso).
        """
        self._client._request(
            "DELETE",
            "/api/v1/client/micropost",
            json={"public_id": public_id},
        )

    def client_vote_micropost(self, public_id: str) -> VoteResponse:
        """
        Vota ou remove o voto de um micropost (toggle).

        Args:
            public_id: ID público do post.

        Returns:
            VoteResponse com user_voted (bool).
        """
        response = self._client._request(
            "PATCH",
            "/api/v1/client/micropost/vote",
            json={"public_id": public_id},
        )
        return VoteResponse(**response.json())
