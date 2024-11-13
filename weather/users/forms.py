from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control me-1'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control me-1'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control me-1'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control me-1'}))
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput(attrs={'class': 'form-control me-1'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
