from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.contrib import messages

from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm, ProfileUserForm


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


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    extra_context = {'title': "Изменение пароля"}

    def get_success_url(self):
        messages.info(self.request, message='Изменения сохранены')
        return reverse_lazy('users:profile')

class ProfileUser(UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        messages.info(self.request, message='Изменения сохранены')
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user