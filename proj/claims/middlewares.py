import re
import time

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if ip:
            if re.match(r"^/(pl|ru|en)/claim_report/error/$", request.path):
                return self.get_response(request)
            request_count = cache.get(ip, 0)
            blocked_until = cache.get(f"{ip}_blocked_until")

            if blocked_until and time.time() < blocked_until:
                return redirect(f'{"/pl/claim_report/error/?status=429"}')

            if blocked_until and time.time() >= blocked_until:
                cache.delete(f"{ip}_blocked_until")
                request_count = 0

            if (
                re.match(r"^/(pl|ru|en)/claim_report/create/$", request.path)
                and request.method == "POST"
            ):
                if request_count >= settings.RATE_LIMIT_MAX_REQUESTS:
                    cache.set(
                        f"{ip}_blocked_until",
                        time.time() + settings.RATE_LIMIT_BLOCK_TIME,
                    )
                    cache.delete(ip)
                    return redirect(f'{"/pl/claim_report/error/?status=429"}')
                else:
                    cache.set(
                        ip, request_count + 1, timeout=settings.RATE_LIMIT_TIMEOUT
                    )

        response = self.get_response(request)
        return response


class CustomErrorStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if "status" in request.GET:
            try:
                status_code = int(request.GET["status"])
                response.status_code = status_code
            except ValueError:
                pass
        return response
