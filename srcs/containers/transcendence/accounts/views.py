from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django_otp import user_has_device
from django_otp.forms import OTPTokenForm

@login_required
def redirect_to_2fa_setup(request):
    print("redirect_to_2fa_setup...")
    setup_url = reverse('two_factor:setup')
    return JsonResponse({'setup_url': setup_url})

def redirect_to_2fa_login(request):
    print("redirect_to_2fa_login...")
    setup_url = reverse('two_factor:login')
    return JsonResponse({'setup_url': setup_url})


def login_view(request):
    print("login_view...")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user_has_device(user):  # Check if user has a 2FA device
                login(request, user)
                if not request.user.is_verified():
                    otp_form = OTPTokenForm(user=request.user)
                    if request.is_ajax():
                        return JsonResponse({'success': True, 'otp_required': True, 'otp_url': '/otp/'})
                else:
                    return JsonResponse({'success': True, 'otp_required': False})
            else:
                login(request, user)
                return JsonResponse({'success': True, 'otp_required': False})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def otp_verification_view(request):
    print("otp_verification_view...")
    if request.method == 'POST':
        otp_form = OTPTokenForm(user=request.user, data=request.POST)
        if otp_form.is_valid():
            otp_form.save()  # Marks the OTP as verified
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid OTP'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})