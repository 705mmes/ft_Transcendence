from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode, base64
from base64 import b64encode
from io import BytesIO
from authentication.models import User
from django.urls import reverse
from django.http import JsonResponse
from django_otp.forms import OTPTokenForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

@login_required
def redirect_to_2fa_setup(request):
    print("User:", request.user)
    user = User.objects.get(username=request.user)
    try:
        device = TOTPDevice.objects.get(user=request.user, name='default')
    except MultipleObjectsReturned:
        device = TOTPDevice.objects.filter(user=request.user, name='default').first()
        print("Multiple devices found. Using the first one.")
    except ObjectDoesNotExist:
        device = None
        print("Device does not exist. Creating a new one.")
        device = TOTPDevice.objects.create(user=request.user, name='default')
    
    if request.method == 'POST':
        form = OTPTokenForm(data=request.POST, user=request.user)
        
        if form.is_valid():
            print("form_is_valid")
            token = form.cleaned_data['otp_token']
            print("Device:", device, "Token:", token)
    
            if device and device.verify_token(token):
                user.twofa_submitted = True
                user.save()
                return JsonResponse({'success': True, 'redirect_url': '/game'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid OTP token.'})
        else:
            print("Form errors:", form.errors)
            return JsonResponse({'success': False, 'error': 'Invalid form submission.'})
    
    else:
        form = OTPTokenForm(user=request.user)
    if device:
        qr_code_img = qrcode.make(device.config_url)
        buffer = BytesIO()
        qr_code_img.save(buffer)
        buffer.seek(0)
        encoded_img = b64encode(buffer.read()).decode()
        qr_code_data = f'data:image/png;base64,{encoded_img}'
    else:
        qr_code_data = None
        print("Error: No device")       
    
    return render(request, 'setup.html', {'form': form, 'qr_url': qr_code_data})

def redirect_to_login(request):
    print("redirect_to_2fa_login...")
    return render(request, 'login.html')

@login_required
def redirect_to_checker(request):
    print("redirect_to_checker...")
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        try:
            device = TOTPDevice.objects.get(user=request.user, name='default')
        except MultipleObjectsReturned:
            device = TOTPDevice.objects.filter(user=request.user, name='default').first()
            print("Multiple devices found. Using the first one.")
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'No Device found.'})
            
        form = OTPTokenForm(data=request.POST, user=request.user)
        if form.is_valid():
            token = form.cleaned_data['otp_token']
            if device and device.verify_token(token):
                return JsonResponse({'success': True, 'redirect_url': '/game'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid OTP token.'})
        else:
            print("Form errors:", form.errors)
            return JsonResponse({'success': False, 'error': 'Invalid form submission.'})
    else:
        form = OTPTokenForm(user=request.user)
        return render(request, 'checker.html', {'form': form})



