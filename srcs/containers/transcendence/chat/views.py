from django.shortcuts import render

from django.shortcuts import render

def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def social(request):
    return render(request, "social.html")

def profile(request):
    return render(request, "authentication/../profile_page/templates/authentication/profile.html")

def game(request):
    return render(request, "game/game.html")