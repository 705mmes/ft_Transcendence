from django.shortcuts import render
def canvas(request):
    return render(request, 'game/canvas.html')

def game(request):
    return render(request, 'game/game.html')

def scripts(request):
    return render(request, 'game/scripts.html')

def social(request):
    all_users = User.objects.all()
    return render(request, 'authentication/social.html', {'all_users': all_users})

def chat(request):
    return render(request, 'chat/chat.html')