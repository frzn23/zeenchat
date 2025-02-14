from django.contrib.sessions.middleware import SessionMiddleware
from .redis_manager import update_user_status

class UserStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # set user as online when they make a request
        if request.user.is_authenticated:
            update_user_status(request.user.username, 'online')
        
        response = self.get_response(request)
        
        # update status when session expires
        if hasattr(request, 'user') and not request.user.is_authenticated:
            session = getattr(request, 'session', None)
            if session and session.is_empty():
                username = session.get('_auth_user_username')
                if username:
                    update_user_status(username, 'offline')
        
        return response 