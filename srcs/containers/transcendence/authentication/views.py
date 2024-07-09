from django.shortcuts import render
from authentication.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def authentication(request):
    context = {
        'login_form': LoginForm,
    }
    if (request.user.is_authenticated):
        return render(request, 'authentication/game.html')
    else:
       return render(request, 'authentication/auth_page.html', context)

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
                return (render(request, 'authentication/game.html'))
            else:
                return (HttpResponse('Error'))

def logout_btn(request):
    logout(request)
    context = {'login_form': LoginForm}
    return render(request, 'authentication/btn_page.html', context)

def game(request):
    return render(request, 'authentication/canvas.html')
