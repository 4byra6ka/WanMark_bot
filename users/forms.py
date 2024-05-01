from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "Пользователь", 'class': 'form-control', 'type': 'username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': "Пароль", 'class': 'form-control', 'type': 'password'}))


class TGPasswordResetForm(forms.Form):
    email = forms.CharField(
        label=_("Username"),
        max_length=254,
        # widget=forms.CharField(attrs={"autocomplete": "username"}),
    )
