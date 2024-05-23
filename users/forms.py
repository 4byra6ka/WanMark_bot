from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "Пользователь", 'class': 'form-control', 'type': 'username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': "Пароль", 'class': 'form-control', 'type': 'password'}))


class UserChangeForm(forms.ModelForm):
    """Форма для обновления пользователей. Включает все поля пользователя, но заменяет поле пароля полем отображения
    хеша пароля, отключенным администратором."""

    password = ReadOnlyPasswordHashField(label="Хеш пароля")

    class Meta:
        model = User
        fields = ["username", "password", "is_active"]


class UserCreationForm(forms.ModelForm):
    """Форма для создания новых пользователей. Включает в себя все необходимое поля, а также повторный пароль."""

    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        return user
