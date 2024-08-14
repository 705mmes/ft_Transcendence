import json
from urllib.parse import quote
import requests
from django.conf import settings
from django.views import View
from django.shortcuts import render
from authentication.forms import LoginForm, RegistrationForm
from .models import User
import logging
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods

logger = logging.getLogger('authentication')

UID = settings.OAUTH_CLIENT_ID
SECRET = settings.OAUTH_CLIENT_SECRET
def authentication(request):
    print("Authentication view is called")
    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
    }
    if request.user.is_authenticated:
        return render(request, 'game/game.html')
    return render(request, 'authentication/auth_page.html', context)

def get_redirect_uri(request):
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

class StartOAuthView(View):
    def get(self, request):
        redirect_uri = get_redirect_uri(request)
        encoded_redirect_uri = quote(redirect_uri, safe='')
        authorization_endpoint = "https://api.intra.42.fr/oauth/authorize"
        auth_url = f"{authorization_endpoint}?client_id={settings.OAUTH_CLIENT_ID}&redirect_uri={encoded_redirect_uri}&response_type=code"
        print(f"Redirecting to: {auth_url}")
        return HttpResponseRedirect(auth_url)

@csrf_exempt
@require_http_methods(["POST"])
def exchange_token(request):
    if request.method == 'POST':
        redirect_uri = get_redirect_uri(request)
        try:
            data = json.loads(request.body)
            code = data.get('code')
            response = requests.post(
                "https://api.intra.42.fr/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": UID,
                    "client_secret": SECRET,
                    "redirect_uri": redirect_uri,
                    "code": code
                }
            )
            response.raise_for_status()
            return JsonResponse(response.json())
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return JsonResponse({'error': 'Failed to exchange token.'}, status=500)

@csrf_exempt
def fetch_user_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            access_token = data.get('accessToken')
            response = requests.get(
                "https://api.intra.42.fr/v2/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()
            return JsonResponse(response.json())
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return JsonResponse({'error': 'Failed to fetch user data.'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')

            if not username or not email:
                return JsonResponse({'error': 'Username and email are required.'}, status=400)

            user = User.objects.filter(username=username).first()
            if user:
                if user.is_active:
                    user = authenticate(request, username=username, password='defaultPass')
                    if user is not None:
                        login(request, user)
                        return JsonResponse({'message': 'User logged in successfully'})
                    return JsonResponse({'error': 'Authentication failed.'}, status=500)
                return JsonResponse({'error': 'User account is inactive.'}, status=403)
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='defaultPass'  # Ideally, use a secure password or method to set the password
                )
                user = authenticate(request, username=username, password='defaultPass')
                if user is not None:
                    login(request, user)
                    return JsonResponse({'message': 'User registered and logged in successfully'})
                return JsonResponse({'error': 'Authentication failed after registration.'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

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
                login(request, user)
                return render(request, 'game/game.html')
            else:
                return HttpResponse('Invalid credentials, please try again.')
        else:
            return render(request, 'authentication/auth_page.html',
                          {'login_form': form, 'registration_form': RegistrationForm()})
    else:
        form = LoginForm()
    return render(request, 'authentication/auth_page.html',
                  {'login_form': form, 'registration_form': RegistrationForm()})


def logout_btn(request):
    logout(request)
    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
    }
    return render(request, 'authentication/btn_page.html', context)


def social(request):
    return render(request, 'authentication/social.html')
