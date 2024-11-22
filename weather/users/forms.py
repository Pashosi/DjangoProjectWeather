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
    email = forms.EmailField(label='E-mail (не обязательно)', required=False, widget=forms.TextInput(attrs={'class': 'form-control me-1'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            return email
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует!')
        return email