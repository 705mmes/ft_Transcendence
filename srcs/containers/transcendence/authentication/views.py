from django.shortcuts import render
from authentication.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def authentication(request):
    return render(request, 'index.html')

def login_popup(request):
    context = {
        'login_form': LoginForm,
    }
    return render(request, 'authentication/login_popup.html', context)

def registration_popup(request):
    return render(request, 'authentication/registration_popup.html')

def login_session(request):
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if (form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print(request.POST['username'])
            print(request.POST['password'])
            if user is not None:
                login(request, user)
                return (render(request, 'authentication/canvas.html'))
            else:
                return (HttpResponse('Error'))