import json
from urllib.parse import quote, urlencode
import requests
from django_otp import user_has_device
from django.conf import settings
from django.shortcuts import render, redirect
from authentication.forms import LoginForm, RegistrationForm
from .models import User
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django_otp.plugins.otp_totp.models import TOTPDevice
import random
import string
from .decorators import custom_login_required


def generate_password():
    length = random.randint(8, 32)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def authentication(request):
    context = {
        'login_form': LoginForm,
        'registration_form': RegistrationForm,
    }
    return render(request, 'authentication/auth_page.html', context)


def get_redirect_uri(request):
    hostname = request.get_host()
    redirect_uris = {
        'localhost:8000': 'http://localhost:8000/',
        'k2r3p9:8000': 'http://k2r3p9:8000/',
        'k2r3p10:8000': 'http://k2r3p10:8000/',
        'k2r3p8:8000': 'http://k2r3p8:8000/',
        '127.0.0.1:8000': 'http://127.0.0.1:8000/',
        '0.0.0.0:8000': 'http://0.0.0.0:8000/',
        '192.168.1.17:8000': 'http://192.168.1.17:8000/',
        'localhost:4443': 'https://localhost:4443/',
        'k2r3p9:4443': 'https://k2r3p9:4443/',
        'k2r3p10:4443': 'https://k2r3p10:4443/',
        'k2r3p8:4443': 'https://k2r3p8:4443/',
        '127.0.0.1:4443': 'https://127.0.0.1:4443/',
        '0.0.0.0:4443': 'https://0.0.0.0:4443/',
        '192.168.1.17:4443': 'https://192.168.1.17:4443/'
    }
    return redirect_uris.get(hostname)


def start_oauth2_flow(request):
    REDIRECT_URI = get_redirect_uri(request)
    authorization_endpoint = "https://api.intra.42.fr/oauth/authorize"
    params = {
        'client_id': settings.OAUTH_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
    }
    auth_url = f"{authorization_endpoint}?{urlencode(params)}"
    return redirect(auth_url)


def oauth_callback(request):
    REDIRECT_URI = get_redirect_uri(request)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    code = body.get('code')

    if not code:
        return JsonResponse({'error': 'Authorization code not provided'}, status=400)

    token_endpoint = "https://api.intra.42.fr/oauth/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.OAUTH_CLIENT_ID,
        'client_secret': settings.OAUTH_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code,
    }
    print(data)
    response = requests.post(token_endpoint, data=data)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch access token'}, status=response.status_code)

    access_token = response.json().get('access_token')

    api_endpoint = "https://api.intra.42.fr/v2/me"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get(api_endpoint, headers=headers)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch protected data'}, status=response.status_code)

    user_data = response.json()
    username = user_data.get('login')
    email = user_data.get('email')
    image_data = user_data.get('image', {})
    main_image_link = image_data.get('link')

    username = username + "_42_intra"
    result = register_api(username, email, request, main_image_link)
    print("Sending response")
    if result['status'] == 'success':
        user = User.objects.get(username=username)
        profile_picture_url = user.get_profile_picture()
        return JsonResponse({
            'message': 'User registered and logged in successfully.',
            'profile_picture': profile_picture_url
        }, status=200)
    else:
        return JsonResponse({'error': result['message']}, status=400)


def register_api(username, email, request, image):
    if User.objects.filter(username=username).exists():
        return {'status': 'success', 'message': 'User registered and logged in successfully.'}
    password = generate_password()

    print("Creating user...")
    user = User.objects.create_user(username=username, email=email, password=password, profile_picture_url=image, is_42=True)
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return {'status': 'success', 'message': 'User registered and logged in successfully.'}
    else:
        return {'status': 'error', 'message': 'Authentication failed.'}


def register(request):
    # faut interdir ces fdp de users d'utiliser _42_intra
    if (request.method == 'POST'):
        print('Registration')
        form = RegistrationForm(request.POST)
        if (form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            if user is not None:
                print("User is OK")
                login(request, user)
                return (render(request, 'game/game.html'))
            else:
                return (HttpResponse('Error'))

def login_session(request):
    print("login session")
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_authenticated:
                    if user_has_device(user):
                        if user.twofa_submitted == False:
                            print("Need to delete TOTPDevice")
                            device = TOTPDevice.objects.get(user=user, name='default')
                            device.delete()
                            login(request, user)
                            return JsonResponse({'success': True, 'redirect_url': '/game'})
                        else:
                            print("Redirecting to 2FA checker page")
                            login(request, user)
                            return JsonResponse({'success': True, 'redirect_url': '/account/redirect/checker'})
                    else:
                        print("Logging in and redirecting to game page")
                        login(request, user)
                        return JsonResponse({'success': True, 'redirect_url': '/game'})
                else:
                    print("Anonymous user detected. Blocking login.")
                    return JsonResponse({'success': False, 'error': 'Anonymous users cannot log in'}, status=400)
            else:
                print("Invalid login credentials")
                return JsonResponse({'success': False, 'error': 'Invalid login credentials'}, status=400)
        else:
            print("Form validation failed")
            return JsonResponse({'success': False, 'error': 'Form is invalid'}, status=400)
    else:
        print("render auth_page")
        form = LoginForm()
        return render(request, 'authentication/auth_page.html', {'login_form': form})



@custom_login_required
def logout_btn(request):
    print("logout view is called")
    logout(request)
    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
    }
    return render(request, 'authentication/btn_page.html', context)

@custom_login_required
def social(request):
    return render(request, 'authentication/social.html')
