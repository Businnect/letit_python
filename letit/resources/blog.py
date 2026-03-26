from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from letit.schemas.blog import BlogResponse, BlogListResponse

if TYPE_CHECKING:
    from ..client import LetIt


class BlogResource:
    def __init__(self, client: "LetIt"):
        self._client = client

    def client_get_admin_blog(self) -> Optional[BlogResponse]:
        """
        Retorna um artigo público do admin.

        Returns:
            BlogResponse ou None se não houver artigo.
        """
        response = self._client._request("GET", "/api/v1/client/admin/blog")
        data = response.json()
        if data is None:
            return None
        return BlogResponse(**data)

    def client_list_admin_blogs(self) -> BlogListResponse:
        """
        Retorna a lista de artigos públicos do admin.

        Returns:
            BlogListResponse com list, total_list e total_pages.
        """
        response = self._client._request("GET", "/api/v1/client/admin/blog/list")
        return BlogListResponse(**response.json())
