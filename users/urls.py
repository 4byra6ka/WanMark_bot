from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.urls import path, include

from users.apps import UserConfig
from users.views import CustomLoginView

app_name = UserConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
