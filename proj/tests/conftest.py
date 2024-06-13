import os

import django

import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")
django.setup()

from django.conf import settings
from django.core.cache import cache

from rest_framework.test import APIClient

from rest_framework_simplejwt.tokens import RefreshToken

from claims.models import ClaimReport

from django.contrib.auth.models import User
from django.utils.translation import activate, get_language


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(username, password):
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return user, str(refresh.access_token)

    return _create_user


@pytest.fixture
def create_claim_report():
    def _create_claim_report(**kwargs):
        return ClaimReport.objects.create(**kwargs)

    return _create_claim_report


@pytest.fixture
def rate_limit_settings():
    original_max_requests = settings.RATE_LIMIT_MAX_REQUESTS
    original_timeout = settings.RATE_LIMIT_TIMEOUT
    original_block_time = settings.RATE_LIMIT_BLOCK_TIME

    settings.RATE_LIMIT_MAX_REQUESTS = 5
    settings.RATE_LIMIT_TIMEOUT = 1
    settings.RATE_LIMIT_BLOCK_TIME = 2

    yield

    settings.RATE_LIMIT_MAX_REQUESTS = original_max_requests
    settings.RATE_LIMIT_TIMEOUT = original_timeout
    settings.RATE_LIMIT_BLOCK_TIME = original_block_time


@pytest.fixture
def clear_rate_limit_cache():
    yield
    cache.clear()


@pytest.fixture
def activate_language():
    def _activate_language(language_code):
        activate(language_code)
        return get_language()

    return _activate_language
