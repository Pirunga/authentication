import time
import logging

logger = logging.getLogger(__name__)

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        method = request.method
        path = request.get_full_path()
        status = response.status_code
        user_email = "No User Info"
        if request.user.is_authenticated:
            user_email = f"User: {request.user.email}"

        logger.info(f"\n{method} {path} - {status} - {user_email} - {duration:.2f}s\n")

        return response