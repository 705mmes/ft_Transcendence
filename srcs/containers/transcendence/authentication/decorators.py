from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

def custom_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('nope')
    return _wrapped_view

def profile_modify(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_42:
                return HttpResponse('nope')
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view
