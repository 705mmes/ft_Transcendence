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

def authentication(request):
    print("authentication view is called")
    context = {
        'login_form': LoginForm,
        'registration_form': RegistrationForm,
    }
    if (request.user.is_authenticated):
        return render(request, 'game/game.html')
    else:
        return render(request, 'authentication/auth_page.html', context)

def get_redirect_uri(request):
    print("get_redirect_uri view is called")
    hostname = request.get_host()
    redirect_uris = {
        'localhost:8000': 'http://localhost:8000/',
        'k2r3p9:8000': 'http://k2r3p9:8000/',
        'k2r3p10:8000': 'http://k2r3p10:8000/',
        'k2r3p8:8000': 'http://k2r3p8:8000/',
        '127.0.0.1:8000': 'http://127.0.0.1:8000/',
        '0.0.0.0:8000': 'http://0.0.0.0:8000/'
    }
    return redirect_uris.get(hostname, 'http://localhost:8000/')

def start_oauth2_flow(request):
    print("start_oauth2_flow view is called")
    REDIRECT_URI = get_redirect_uri(request)
    authorization_endpoint = "https://api.intra.42.fr/oauth/authorize"
    params = {
        'client_id': settings.OAUTH_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
    }
    print(params)
    auth_url = f"{authorization_endpoint}?{urlencode(params)}"
    print(auth_url)
    return redirect(auth_url)

def oauth_callback(request):
    print("oauth_callback view is called")
    REDIRECT_URI = get_redirect_uri(request)
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Authorization code not provided'}, status=400)

    token_endpoint = "https://api.intra.42.fr/oauth/token"
    print("token_endpoint: ", token_endpoint)
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.OAUTH_CLIENT_ID,
        'client_secret': settings.OAUTH_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code,
    }
    print("data:", data)
    response = requests.post(token_endpoint, data=data)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch access token'}, status=response.status_code)

    access_token = response.json().get('access_token')
    print(access_token)
    # You can now use this access token to fetch protected resources
    return fetch_protected_data(access_token)

def fetch_protected_data(access_token):
    print("fetch_protected_data view is called")
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

    result = register_api(username, email)
    print(result)

def register_api(username, email):
    print("registering, username:", username, "email:", email)
    # Generate a secure random password
    password = "test"

    # Create a new user
    if User.objects.filter(username=username).exists():
        return {'status': 'error', 'message': 'Username already exists.'}

    user = User.objects.create_user(username=username, email=email, password=password)

    # Authenticate and log in the user
    user = authenticate(username=username, password=password)
    if user:
        return {'status': 'success', 'message': 'User registered and logged in successfully.'}
    else:
        return {'status': 'error', 'message': 'Authentication failed.'}

def register(request):
    print("register view is called")
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
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if (form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print(request.POST['username'])
            print(request.POST['password'])
            if user is not None:
                login(request, user)
                return (render(request, 'game/game.html'))
            else:
                return (HttpResponse('Error'))


def logout_btn(request):
    print("logout view is called")
    logout(request)
    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
    }
    return render(request, 'authentication/btn_page.html', context)


def social(request):
    return render(request, 'authentication/social.html')
