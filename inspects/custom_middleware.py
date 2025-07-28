from django.http import HttpResponse
from django.contrib.auth import logout
from inspects.models import session_mgmt, login_history


class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        session_key = request.session.session_key
        if session_key and request.user.is_authenticated:
            if not session_mgmt.objects.filter(username = request.user, session_key = session_key).exists():
                import datetime
                login_history.objects.filter(username = request.user,session_key = session_key).update(logout_date_time = datetime.datetime.now())
                logout(request)
                return HttpResponse('It looks like there is another active session currently. Please Login again or contact support if you need immediate assistance. ')
        response = self.get_response(request)
        return response
    

