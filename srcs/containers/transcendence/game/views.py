from django.shortcuts import render
from authentication.models import User
from authentication.forms import LoginForm, RegistrationForm
from .models import TournamentLobby
from django.db.models import Q

def canvas(request):
    return render(request, 'game/canvas.html')

def game(request):
    return render(request, 'game/game.html')

def scripts(request):
    return render(request, 'game/scripts.html')


def social(request):
    all_users = User.objects.all()
    return render(request, 'authentication/social.html', {'all_users': all_users})


def match_1v1(request):
    return render(request, "game/1v1_match.html")


def tournament(request):
    return render(request, "game/tournament.html")


def tournament_bracket(request):
    user = request.user
    lobby_queryset = TournamentLobby.objects.filter(Q(P1=user) | Q(P2=user) | Q(P3=user) | Q(P4=user))
    lobby = lobby_queryset.first()
    return render(request, "game/tournament_bracket.html", {'lobby': lobby})