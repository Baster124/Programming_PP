import pytest
from package import client


def test_app():
    resp = client.get('/')
    assert resp.status_code == 200
