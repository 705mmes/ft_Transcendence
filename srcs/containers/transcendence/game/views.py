from django.shortcuts import render


def game(request):
    return render(request, 'game/canvas.html')

def scripts(request):
    return render(request, 'game/scripts.html')