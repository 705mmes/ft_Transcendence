from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django_otp import user_has_device
from django_otp.forms import OTPTokenForm
from django.contrib.auth import get_user_model

@login_required
def redirect_to_2fa_setup(request):
    print("redirect_to_2fa_setup...")
    setup_url = reverse('two_factor:setup')
    return JsonResponse({'setup_url': setup_url})


def redirect_to_login(request):
    print("redirect_to_2fa_login...")
    return render(request, 'login.html')


def redirect_to_checker(request):
    print("redirect_to_checker...")
    return render(request, 'checker.html')


def two_factor_login(request):
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('login')

    user = get_user_model().objects.get(id=user_id)

    if request.method == 'POST':
        form = OTPTokenForm(user, request.POST)
        if form.is_valid():
            form.save() 
            login(request, user)
            return redirect('game/')
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid token'})
    else:
        form = OTPTokenForm(user)
        return render(request, 'login.html', {'form': form})

