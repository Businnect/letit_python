from letit.settings import DEFAULT_API_SERVER
from letit.resources.micropost import MicropostResource
from letit.resources.job import JobResource
from letit.resources.blog import BlogResource
import requests


class LetIt:
    """
    Cliente para a API LetIt.

    Args:
        api_token: Seu token de API. Gere em https://letit.com/settings/developer
        base_url: URL base da API. Padrão: servidor LetIt.

    Example:
        client = LetIt(api_token="seu_token_aqui")
    """

    def __init__(
        self,
        api_token: str,
        base_url: str = DEFAULT_API_SERVER,
    ) -> None:
        self.api_token = api_token
        self.base_url = base_url
        self._headers = {"USER-API-TOKEN": api_token}

        self.micropost = MicropostResource(self)
        self.job = JobResource(self)
        self.blog = BlogResource(self)

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        extra_headers = kwargs.pop("headers", {})
        headers = {**self._headers, **extra_headers}
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response
