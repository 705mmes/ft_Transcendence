from django.shortcuts import render
from django.shortcuts import render, redirect
from two_factor.forms import TOTPDeviceForm
from two_factor.views import LoginView, ProfileView
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'account/login.html'

class CustomProfileView(ProfileView):
    template_name = 'account/profile.html'

def activate_2fa(request):
    form = TOTPDeviceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'account/activate_2fa.html', {'form': form})

