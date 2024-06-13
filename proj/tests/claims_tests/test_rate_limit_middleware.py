import time

from django.core.cache import cache

import pytest


@pytest.mark.django_db
def test_rate_limit_normal_usage(api_client, create_user, rate_limit_settings):
    user, token = create_user("testuser", "testpassword")
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    response = api_client.post("/claim_report/create/", data={})
    assert response.status_code != 429


@pytest.mark.django_db
def test_rate_limit_exceeded(api_client, create_user, rate_limit_settings):
    user, token = create_user("testuser", "testpassword")
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    for _ in range(5):
        api_client.post("/en/claim_report/create/", data={})

    response = api_client.get("/en/claim_report/error/?status=429", data={})
    assert response.status_code == 429
    assert "Too many requests. Try again later." in response.content.decode()


@pytest.mark.django_db
def test_rate_limit_resets_after_time(api_client, create_user, rate_limit_settings):
    user, token = create_user("testuser", "testpassword")
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    for _ in range(5):
        api_client.post("/claim_report/create/", data={})

    time.sleep(2)

    response = api_client.post("/claim_report/create/", data={})
    assert response.status_code != 429


@pytest.mark.django_db
def test_rate_limit_cache_cleanup(api_client, create_user, rate_limit_settings):
    user, token = create_user("testuser", "testpassword")
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    ip = "127.0.0.1"
    cache.set(ip, 5, timeout=1)
    cache.set(f"{ip}_blocked_until", time.time() + 2)

    response = api_client.get("/en/claim_report/error/?status=429", data={})
    assert response.status_code == 429
    assert "Too many requests. Try again later." in response.content.decode()

    time.sleep(2)

    cache.delete(ip)
    cache.delete(f"{ip}_blocked_until")

    response = api_client.post("/en/claim_report/create/", data={})
    assert response.status_code != 429


@pytest.mark.django_db
def test_rate_limit_get_requests(api_client, rate_limit_settings):
    for _ in range(10):
        api_client.get("/pl/claim_report/create/")

    response = api_client.get("/pl/claim_report/create/")
    assert response.status_code == 200
