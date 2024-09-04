from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django_otp.forms import OTPTokenForm
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode, base64
from io import BytesIO
from django.urls import reverse
from django.http import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile


@login_required
def redirect_to_2fa_setup(request):
	user = request.user

	print("Get or create a TOTP device for the user")
	device, created = TOTPDevice.objects.get_or_create(user=user, name='default')

	print("generating qrcode")
	qr = qrcode.make(device.config_url)
	buffer = BytesIO()
	qr.save(buffer, format='PNG')
	qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
     
	form = OTPTokenForm(user)

	if request.method == 'POST':
		print("catched otp-form fetch")
		form = OTPTokenForm(user, request.POST)
		if form.is_valid():
			form.save()  # Mark the OTP as verified
			return JsonResponse({'success': True, 'redirect_url': reverse('game')})
		else:
			return JsonResponse({'success': False, 'error': 'Invalid token, please try again.', 'redirect_url': reverse('profile_modify')})

	return render(request, 'setup.html', {'form': form, 'qr_image': qr_image})


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

