# chats/middleware.py

from datetime import datetime, time
import logging
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define access hours (e.g., 08:00 to 18:00)
        self.allowed_start = time(8, 0, 0)
        self.allowed_end = time(18, 0, 0)

    def __call__(self, request):
        now = datetime.now().time()
        if not (self.allowed_start <= now <= self.allowed_end):
            return HttpResponseForbidden("Access not allowed at this time.")
        return self.get_response(request)
