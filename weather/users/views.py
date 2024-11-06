from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import LoginUserForm, RegisterUserForm


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                # return HttpResponseRedirect(reverse('home'))
                return HttpResponse("home")
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'title':'Регистрация', 'form': form})

def logout_user(request):
    return HttpResponse("logout")

def register_user(request):
    form = RegisterUserForm()
    return render(request, 'users/register.html', {'title':'Регистрация', 'form': form})

