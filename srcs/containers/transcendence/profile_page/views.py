from django.shortcuts import render
from authentication.forms import ModifiedProfileForm
from django.http import HttpResponse
from game.models import GameHistory
from django.db.models import Q
from authentication.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
    
# Create your views here.
def profile_update(request):
    user = User.objects.get(id=request.user.id)
    if (request.method == 'POST'):
        form = ModifiedProfileForm(request.POST, request.FILES, instance=user)
        print('Profile picture:', request.FILES.get('profile_picture'))
        if (form.is_valid()):
            if (form.cleaned_data['new_password']):
                try:
                    validate_password(form.cleaned_data['new_password'], form.cleaned_data['new_password_repeat'])
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)
                    form.save()
                    return HttpResponse('Password updated successfully')
                except ValidationError:
                    return HttpResponse('wrong password')
            form.save()
            return HttpResponse('Success')
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
        'target': 'me',
        'player': me,
        'game': game_history
    }
    return render(request, 'profile/profile.html', context)

def friend_profile(request):
    target_name = request.GET.get('target_name')
    print(target_name)
    target_user = User.objects.filter(username=target_name).get()
    test = GameHistory.objects.filter(Q(History1=target_user) | Q(History2=target_user))

    print(test)
    five_last_game = list(test)[-5:]
    game_history = []
    for game in reversed(five_last_game):

        if (game.History1 == target_user):
            game_history.append({
                'User1': {'score': game.Score1, 'username': game.History1.username},
                'User2': {'score': game.Score2, 'username': game.History2.username}
            })
        else:
            game_history.append({
                'User1': {'score': game.Score2, 'username': game.History2.username},
                'User2': {'score': game.Score1, 'username': game.History1.username}
            })
    context = {
        'target': 'friend',
        'player': target_user,
        'game': game_history,
    }
    return render(request, 'profile/profile.html', context)