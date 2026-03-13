# Unit tests

import httpx
import pytest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from client import LetIt

# $pip install -e .
# $LETIT_API_TOKEN=yours python -m pytest letit/tests/test_letit_integration.py -v -s
# @pytest.mark.skip(reason="already tested")
def test_client_create_micropost():
    client = LetIt(api_token=os.environ["LETIT_API_TOKEN"])
    try:
        response = client.micropost.client_create_micropost(title="Test", body="Hello")
        assert response.public_id is not None
    except Exception as e:
        if hasattr(e, 'response'):
            print(repr(e.response.text))
        raise


@pytest.mark.skip(reason="already tested")
def test_create_user_job_with_company():
    client = LetIt(api_token=os.environ["LETIT_API_TOKEN"])
    try:
        with open("letit/tests/test_logo.png", "rb") as f:
            response = client.job.client_create_user_job_with_company(
                company_name="LetIt",
                company_description="A test company.",
                company_logo=("logo.png", f, "image/png"),
                company_website="https://letit.com",
                job_title="Test Engineers",
                job_description="Write tests all day.",
                job_how_to_apply="https://letit.com/apply",
                job_skills="Python, pytest",
            )
            assert response.slug is not None
    except Exception as e:
        if hasattr(e, 'response'):
            print(repr(e.response.text))
        raise