# Testes unitários
# pip install -e .
# pytest letit/tests/test_letit_unit.py -v

import pytest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from client import LetIt
from settings import DEFAULT_API_SERVER


@pytest.fixture
def client():
    return LetIt(api_token="test_token")


# --- Client ---

def test_init(client):
    assert client.api_token == "test_token"
    assert client._headers == {"USER-API-TOKEN": "test_token"}
    assert client.base_url == DEFAULT_API_SERVER


@patch("letit.client.requests.request")
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


@patch("letit.client.requests.request")
def test_request_raises_on_error(mock_request, client):
    import requests as req
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = req.exceptions.HTTPError("404")
    mock_request.return_value = mock_response

    with pytest.raises(req.exceptions.HTTPError):
        client._request("GET", "/bad/path")


# --- Micropost ---

@patch("letit.resources.micropost.MultipartEncoder")
def test_create_micropost(mock_encoder, client):
    mock_m = MagicMock()
    mock_m.content_type = "multipart/form-data; boundary=abc"
    mock_encoder.return_value = mock_m

    mock_response = MagicMock()
    mock_response.json.return_value = {"public_id": "abc123", "link": "https://letit.com/p/abc123"}
    client._request = MagicMock(return_value=mock_response)

    result = client.micropost.client_create_micropost(title="Teste", body="Olá mundo")

    assert result.public_id == "abc123"
    assert result.link == "https://letit.com/p/abc123"
    client._request.assert_called_once()


def test_delete_micropost(client):
    client._request = MagicMock()
    client.micropost.client_delete_micropost(public_id="abc123")
    client._request.assert_called_once_with(
        "DELETE",
        "/api/v1/client/micropost",
        json={"public_id": "abc123"},
    )


def test_vote_micropost(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"user_voted": True}
    client._request = MagicMock(return_value=mock_response)

    result = client.micropost.client_vote_micropost(public_id="abc123")

    assert result.user_voted is True
    client._request.assert_called_once_with(
        "PATCH",
        "/api/v1/client/micropost/vote",
        json={"public_id": "abc123"},
    )


# --- Job ---

@patch("letit.resources.job.MultipartEncoder")
def test_create_job(mock_encoder, client):
    mock_m = MagicMock()
    mock_m.content_type = "multipart/form-data; boundary=abc"
    mock_encoder.return_value = mock_m

    mock_response = MagicMock()
    mock_response.json.return_value = {"slug": "dev-python-letit"}
    client._request = MagicMock(return_value=mock_response)

    result = client.job.client_create_user_job_with_company(
        company_name="LetIt",
        company_description="Fazemos coisas.",
        company_website="https://letit.com",
        job_title="Dev Python",
        job_description="Desenvolver APIs.",
        job_how_to_apply="https://letit.com/apply",
    )

    assert result.slug == "dev-python-letit"


def test_delete_job(client):
    client._request = MagicMock()
    client.job.client_delete_job(slug="dev-python-letit")
    client._request.assert_called_once_with(
        "DELETE",
        "/api/v1/client/job",
        json={"slug": "dev-python-letit"},
    )


# --- Blog ---

def test_get_admin_blog_none(client):
    mock_response = MagicMock()
    mock_response.json.return_value = None
    client._request = MagicMock(return_value=mock_response)

    result = client.blog.client_get_admin_blog()
    assert result is None


def test_list_admin_blogs(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "list": [
            {
                "body": "Conteúdo",
                "category": "ANNOUNCEMENT",
                "is_featured": True,
                "published_at": "2026-03-25T16:17:12.799Z",
                "slug": "meu-artigo",
                "title": "Meu Artigo",
            }
        ],
        "total_list": 1,
        "total_pages": 1,
    }
    client._request = MagicMock(return_value=mock_response)

    result = client.blog.client_list_admin_blogs()
    assert result.total_list == 1
    assert result.list[0].slug == "meu-artigo"
