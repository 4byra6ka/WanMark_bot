from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.urls import path, include

from users.apps import UserConfig
from users.views import CustomLoginView # TGRecoveryPasswordView,

app_name = UserConfig.name

admin.site.site_header = 'WanMark'                    # default: "Django Administration"
admin.site.index_title = 'Сайт для администрирования бота'                 # default: "Site administration"
admin.site.site_title = '' # default: "Django site admin"

urlpatterns = [
    # path('grappelli/', include('grappelli.urls')),
    # path('admin/', admin.site.urls),
    # path('admin/password_reset/', TGRecoveryPasswordView.as_view(), name='admin_password_reset'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]




from users.apps import UserConfig
# from users.views import CustomLoginView



# urlpatterns = [
#     path('', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
    # path('admin/reset_password/', PasswordResetView.as_view(), name='admin_password_reset'),
    # path('register/', RegisterView.as_view(), name='register'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('recovery_password/', RecoveryPasswordView.as_view(), name='recovery_password'),
    # path('success_register/<str:register_uuid>/', verification_user, name='success_register')

# ]