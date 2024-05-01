from django.shortcuts import render
from django.views.generic import FormView

from users.forms import TGPasswordResetForm
from users.models import User


from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LoginView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import UserLoginForm
from users.models import User


class CustomLoginView(FormView):
    model = User
    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {
        'title': 'Авторизация'
    }
    # success_url = redirect('main.main')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/admin/')
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect('/admin/')
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            try:
                user = User.objects.get(username=form.cleaned_data['username'])
            except:
                # messages.error(self.request, 'Неправильный пользователь или пароль')
                messages.add_message(self.request, messages.WARNING,'Неправильный пользователь или пароль')
            if user is not None:
                login(self.request, user)
                # perm_client = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Client))
                # user.user_permissions.add(perm_client.get(codename='add_client'))
                # user.user_permissions.add(perm_client.get(codename='view_client'))
                # user.user_permissions.add(perm_client.get(codename='change_client'))
                # user.user_permissions.add(perm_client.get(codename='delete_client'))
                if self.request.GET.get('next', '') != '':
                    return HttpResponseRedirect(self.request.GET.get('next', ''))
                return redirect('/admin/')
                message = f'Hello {user.username}! You have been logged in'
                return redirect('/admin/')
            else:
                message = 'Login failed!'
        return render(
            self.request, 'users/login.html', context={'form': form, 'message': message})



# class TGRecoveryPasswordView(FormView):
#     """Контроллер восстановления пароля"""
#     model = User
#     template_name = 'users/tg_password_reset_form.html'
#     form_class = TGPasswordResetForm
#     extra_context = {
#         'title': 'Восстановление пароля'
#     }
#
#     def form_valid(self, form, *args, **kwargs):
#         try:
#             recovery_user = User.objects.get(email=form.cleaned_data['email_recovery'])
#             self.object = form
#             if recovery_user and form.is_valid():
#                 password = User.objects.make_random_password()
#                 recovery_user.set_password(password)
#                 recovery_user.save()
#                 send_mail(
#                     subject='Новый пароль',
#                     message=f'Ваш новый пароль: {password}',
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[recovery_user.email]
#                 )
#                 return super().form_valid(form, *args, **kwargs)
#         except:
#             messages.add_message(self.request, messages.WARNING, 'Неправельная почта')
#         return super().form_invalid(form)
#
#     def get_success_url(self):
#         messages.add_message(self.request, messages.INFO,
#                              f'Пароль направлен на Email: {self.object.cleaned_data["email_recovery"]}')
#         return reverse_lazy('users:login')
