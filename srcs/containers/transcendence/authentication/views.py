import json
from django.shortcuts import render
from authentication.forms import LoginForm, RegistrationForm
from .models import User
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create your views here.
def authentication(request):
    context = {
        'login_form': LoginForm,
        'registration_form': RegistrationForm,
    }
    if (request.user.is_authenticated):
        return render(request, 'game/game.html')
    else:
        return render(request, 'authentication/auth_page.html', context)


def api_connection(request):
    if request.method == 'PUT':
        try:
            # Parse JSON body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            # Validate input data
            if not username or not password or not email:
                return HttpResponseBadRequest('Missing required fields')

            # Create user
            user = User.objects.create_user(username=username, password=password, email=email)

            # Authenticate and log in the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'User registered successfully'}, status=201)
            else:
                return HttpResponse('Error in authentication', status=401)
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {str(e)}')

def register(request):
    if (request.method == 'PUT'):
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
    logout(request)
    context = {
        'login_form': LoginForm,
        'registration_form': RegistrationForm,
    }
    return render(request, 'authentication/btn_page.html', context)



def social(request):
    return render(request, 'authentication/social.html')

