import json
from urllib.parse import quote, urlencode
import requests
from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from authentication.forms import LoginForm, RegistrationForm
from .models import User
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django_otp.decorators import otp_required
import random
import string

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
    if (request.user.is_authenticated):
        return render(request, 'game/game.html')
    else:
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
    response = requests.post(token_endpoint, data=data)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch access token'}, status=response.status_code)

    access_token = response.json().get('access_token')
    # You can now use this access token to fetch protected resources

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
        print("Username already taken.")
        return {'status': 'error', 'message': 'Username already taken.(un jour je gererais ca)'}
    password = generate_password()

    print("Creating user...")
    user = User.objects.create_user(username=username, email=email, password=password, profile_picture_url=image, is_42=True)
    # Authenticate and log in the user
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return {'status': 'success', 'message': 'User registered and logged in successfully.'}
    else:
        return {'status': 'error', 'message': 'Authentication failed.'}


def register(request):
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # print("about to call two_factor...")
                # request.session['pre_2fa_user_id'] = user.pk  # Save the user's ID before 2FA
                # return redirect('two_factor:login')  # Redirect to 2FA verification
                login(request, user)
                return (render(request, 'game/game.html'))
            else:
                return HttpResponse('Error: Invalid login credentials')
        else:
            return HttpResponse('Error: Form is not valid')
    else:
        form = LoginForm()
        return render(request, 'authentication/auth_page.html', {'login_form': form})



def logout_btn(request):
    print("logout view is called")
    # request.user.is_connected = False
    # request.user.save()
    logout(request)
    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
    }
    return render(request, 'authentication/btn_page.html', context)


def social(request):
    return render(request, 'authentication/social.html')

# def two_factor_login(request):
#     return render(request, 'two_factor/core/login.html')
