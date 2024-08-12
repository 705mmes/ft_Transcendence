from django.shortcuts import render
from authentication.forms import ModifiedProfileForm
from django.http import HttpResponse
from game.models import GameHistory

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
    print(GameHistory.History1)
    print(GameHistory.History2)
    print(GameHistory.Score1)
    print(GameHistory.Score2)
    return render(request, 'profile/history.html')