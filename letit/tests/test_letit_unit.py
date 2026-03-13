# Unit tests

import httpx
import pytest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from client import LetIt
from settings import DEFAULT_API_SERVER

# $pip install -e .
# $pytest letit/tests/test_letit_unit.py -v
@pytest.fixture
def client():
    return LetIt(api_token="test_token")


def test_init(client):
    assert client.api_token == "test_token"
    assert client._headers == {"USER-API-TOKEN": "test_token"}
    assert client.base_url == DEFAULT_API_SERVER


@patch("letit.client.httpx.request")
def test_request_success(mock_request, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_request.return_value = mock_response

    response = client._request("GET", "/some/path")

    mock_request.assert_called_once_with(
        "GET",
        f"{DEFAULT_API_SERVER}/some/path",
        headers={"USER-API-TOKEN": "test_token"},
    )
    assert response == mock_response


@patch("letit.client.httpx.request")
def test_request_raises_on_error(mock_request, client):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404", request=MagicMock(), response=mock_response
    )
    mock_request.return_value = mock_response

    with pytest.raises(httpx.HTTPStatusError):
        client._request("GET", "/bad/path")