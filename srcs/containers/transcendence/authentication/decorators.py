from django.http import JsonResponse
from django.conf import settings

def custom_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        print("In custom decorator")
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:  
            print("User is not authenticated")
            return JsonResponse({'redirect_url': settings.LOGIN_URL}, status=200)  
    return _wrapped_view


