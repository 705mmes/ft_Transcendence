from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings

def custom_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.method == 'POST':
                return JsonResponse({'error': 'not_authenticated'}, status=401)
            else:
                return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view

def profile_modify(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_42:
                return HttpResponseRedirect('/profile')
            else:
                return view_func(request, *args, **kwargs)
    return _wrapped_view