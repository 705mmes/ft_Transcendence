from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode, base64
from base64 import b64encode
from io import BytesIO
from django.urls import reverse
from django.http import JsonResponse
from django_otp.forms import OTPTokenForm
from django_otp.plugins.otp_totp.models import TOTPDevice

@login_required
def redirect_to_2fa_setup(request):
    print("User:", request.user)
    if request.method == 'POST':
        form = OTPTokenForm(request.POST)
        
        if form.is_valid():
            token = form.cleaned_data['otp_token']
            if request.user.otp_device.verify_token(token):
                return redirect('/game/')
            else:
                form.add_error(None, 'Invalid OTP token.')
        else:
            form.add_error(None, 'Invalid form submission.')
    
    else:
        form = OTPTokenForm(user=request.user)
    
    device, created = TOTPDevice.objects.get_or_create(user=request.user, name='default')
    
    qr_code_img = qrcode.make(device.config_url)
    buffer = BytesIO()
    qr_code_img.save(buffer)
    buffer.seek(0)
    encoded_img = b64encode(buffer.read()).decode()
    qr_code_data = f'data:image/png;base64,{encoded_img}'
    
    return render(request, 'setup.html', {'form': form, 'qr_url': qr_code_data})


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

