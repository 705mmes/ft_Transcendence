from django.shortcuts import render
from authentication.forms import ModifiedProfileForm
from django.http import HttpResponse
from game.models import GameHistory
from django.db.models import Q

# Create your views here.
def profile(request):
    if (request.method == 'POST'):
        form = ModifiedProfileForm(request.POST, request.FILES, instance=request.user)
        print('Profile picture:', request.FILES.get('profile_picture'))
        if (form.is_valid()):
            if (form.cleaned_data['new_password']):
                print(form.cleaned_data['new_password'])
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                form.save()
                return HttpResponse('Password changed')
            form.save()
            return HttpResponse('Success')
        else:
            return HttpResponse('Error')
    else:
        form = ModifiedProfileForm(instance=request.user)
    context = {
        'registration_form': form,
        'player': request.user,
    }
    return render(request, 'profile/profile.html', context)

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
        'game': game_history
    }
    return render(request, 'profile/history.html', context)