from django.shortcuts import render
from authentication.forms import ModifiedProfileForm
from django.http import HttpResponse
from game.models import GameHistory
from django.db.models import Q
from authentication.models import User
from django.views.decorators.csrf import csrf_exempt


#bout de scotch deconnexion
@csrf_exempt
def deconnexion(request):
    request.user.is_connected = False
    request.user.save()
    print('user deconnected')
    return HttpResponse('user disconnected')

    
# Create your views here.
def profile_update(request):
    user = User.objects.get(id=request.user.id)
    if (request.method == 'POST'):
        form = ModifiedProfileForm(request.POST, request.FILES, instance=user)
        print('Profile picture:', request.FILES.get('profile_picture'))
        if (form.is_valid()):
            form.save()
            return HttpResponse('Success')
        else:
            return HttpResponse('Error')
    else:
        form = ModifiedProfileForm(instance=user)
    context = {
        'registration_form': form,
        'player': request.user,
    }
    return render(request, 'profile/player_form.html', context)

def history(request):
    me = request.user
    test = GameHistory.objects.filter(Q(History1=me) | Q(History2=me))

    print(test)
    five_last_game = list(test)[-5:]
    game_history = []
    for game in reversed(five_last_game):

        if (game.History1 == me):
            game_history.append({
                'User1': {'score': game.Score1, 'username': game.History1.username},
                'User2': {'score': game.Score2, 'username': game.History2.username}
            })
        else:
            game_history.append({
                'User1': {'score': game.Score2, 'username': game.History2.username},
                'User2': {'score': game.Score1, 'username': game.History1.username}
            })
    context  ={
        'player': me,
        'game': game_history
    }
    return render(request, 'profile/profile.html', context)