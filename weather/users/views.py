from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from .forms import LoginUserForm, RegisterUserForm



class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    extra_context = {'title':'Авторизация'}

    def get_default_redirect_url(self):
        if self.request.user.is_staff:
            return '/admin/'
        else:
            return '/'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title':'Регистрация'}
    success_url = reverse_lazy('users:login')

