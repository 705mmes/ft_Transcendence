from django.shortcuts import render

def game_reload(request):
    return render(request, 'game/game.html')
def game(request):
    return render(request, 'game/canvas.html')

def scripts(request):
    return render(request, 'game/scripts.html')