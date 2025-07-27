
import logging
from datetime import datetime, timedelta, time
from collections import defaultdict
from django.http import HttpResponseForbidden, JsonResponse

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







class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to store IP: [timestamps of recent POSTs]
        self.message_log = defaultdict(list)
        self.MESSAGE_LIMIT = 5
        self.TIME_WINDOW = timedelta(minutes=1)

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/'):  # adjust path filter if needed
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Remove timestamps older than the time window
            self.message_log[ip] = [
                timestamp for timestamp in self.message_log[ip]
                if now - timestamp <= self.TIME_WINDOW
            ]

            if len(self.message_log[ip]) >= self.MESSAGE_LIMIT:
                return JsonResponse(
                    {"error": "Message rate limit exceeded. Please wait before sending more messages."},
                    status=429
                )

            # Record the new message timestamp
            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip



class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            allowed_roles = ['admin', 'moderator']
            user_role = getattr(request.user, 'role', None)

            if user_role not in allowed_roles:
                return JsonResponse(
                    {"error": "Forbidden: You do not have permission to access this resource."},
                    status=403
                )
        return self.get_response(request)








