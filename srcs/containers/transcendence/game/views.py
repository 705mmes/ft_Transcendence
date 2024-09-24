from django.shortcuts import render
from authentication.models import User
from authentication.forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from authentication.decorators import custom_login_required

@custom_login_required
def canvas(request):
    return render(request, 'game/canvas.html')

@custom_login_required
def game(request):
    return render(request, 'game/game.html')

# @custom_login_required
def scripts(request):
    return render(request, 'game/scripts.html')

@custom_login_required
def social(request):
    all_users = User.objects.all()
    return render(request, 'authentication/social.html', {'all_users': all_users})

@custom_login_required
def match_1v1(request):
    return render(request, "game/1v1_match.html")

@custom_login_required
def tournament(request):
    return render(request, "game/tournament.html")