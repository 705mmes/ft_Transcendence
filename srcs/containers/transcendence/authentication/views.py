from django.shortcuts import render
from authentication.forms import LoginForm, RegistrationForm, ModifiedProfileForm
from .models import User
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout


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


def profile(request):
    if (request.method == 'POST'):
        form = ModifiedProfileForm(request.POST, request.FILES, instance=request.user)
        print('Profile picture:', request.FILES.get('profile_picture'))
        if (form.is_valid()):
            form.save()
    else:
        form = ModifiedProfileForm(instance=request.user)
    context = {
        'registration_form': form,
        'player': request.user,
    }
    return render(request, 'authentication/profile.html', context)

def profile_page(request):
    return render(request, 'authentication/profile_page.html')

def social(request):
    return render(request, 'authentication/social.html')

