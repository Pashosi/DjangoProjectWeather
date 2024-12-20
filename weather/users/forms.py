import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError


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
    email = forms.EmailField(label='E-mail (не обязательно)', required=False, widget=forms.TextInput(attrs={'class': 'form-control me-1'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']

        if re.fullmatch(r'[a-zA-Z0-9.]+', username):
            return username
        else:
            raise ValidationError("Логин должен содержать только буквы латинского алфавита (a–z), цифры (0–9) и точки (.)")

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            return email
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует!')
        return email

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-control me-1'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-control me-1'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control me-1'}))


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-control me-1'})),
    email = forms.CharField(disabled=True, label='Email', widget=forms.TextInput(attrs={'class': 'form-control me-1'})),

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control me-1'}),
            'email': forms.TextInput(attrs={'class': 'form-control me-1'})
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id

        if get_user_model().objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError("Этот email уже используется другим пользователем.")
        return email