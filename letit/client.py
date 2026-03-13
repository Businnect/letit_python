# $pip freeze > requirements.txt
# $pip install -r requirements.txt

from letit.settings import DEFAULT_API_SERVER
from letit.resources.micropost import MicropostResource
from letit.resources.job import JobResource
import requests

class LetIt:
    """
    Client for the LetIt API.

    Args:
        api_token: Your API token. Generate one at https://letit.com/settings/developer
        base_url: Base URL for the API. Defaults to the standard LetIt API server.

    Example:
        client = LetIt(api_token="your_token_here")
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

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        extra_headers = kwargs.pop("headers", {})
        headers = {**self._headers, **extra_headers}
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response