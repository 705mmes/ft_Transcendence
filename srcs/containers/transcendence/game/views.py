from django.shortcuts import render
from authentication.models import User
from authentication.forms import LoginForm, RegistrationForm

def canvas(request):
    return render(request, 'game/canvas.html')

def game(request):
    return render(request, 'game/game.html')

def scripts(request):
    return render(request, 'game/scripts.html')


def social(request):
    all_users = User.objects.all()
    return render(request, 'authentication/social.html', {'all_users': all_users})


def new_game(request):
    return render(request, "game/new_game.html")