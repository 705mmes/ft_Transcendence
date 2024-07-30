from django.shortcuts import render


def canvas(request):
    return render(request, 'game/canvas.html')

def game(request):
    return render(request, 'game/game.html')

def scripts(request):
    return render(request, 'game/scripts.html')