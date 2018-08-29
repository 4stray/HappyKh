import pytest


@pytest.mark.urls('happykh.urls')
def test_index_url(client):
    assert client.get('/').status_code == 404
