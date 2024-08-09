from django.shortcuts import render
from authentication.forms import ModifiedProfileForm
from django.http import HttpResponse

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

def profile_page(request):
    return render(request, 'profile/profile_page.html')