from django.utils import timezone
from .models import UserSession


class UserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            session_key = request.session.session_key
            if session_key:
                UserSession.objects.get_or_create(
                    session_key=session_key,
                    user=request.user,
                    defaults={'created_at': timezone.now()}
                )

        return response
