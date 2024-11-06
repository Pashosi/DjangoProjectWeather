from django import forms
from django.contrib.auth import get_user_model



class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegisterUserForm(forms.ModelForm):
    # login = forms.CharField(label='Логин', max_length=50, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Пароль (повторно)', max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password2')
