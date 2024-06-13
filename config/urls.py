from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from users.forms import UserLoginForm

admin.site.site_header = 'WanMark'
admin.site.index_title = 'Сайт для администрирования бота'
admin.site.site_title = ''
admin.AdminSite.site_url = ''
admin.AdminSite.login_form = UserLoginForm

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def get_app_list(self, request, app_label=None):
    """
    Возвращает отсортированный список всех установленных приложений, которые были зарегистрировался на этом сайте.
    """
    # Получить исходный список.
    app_dict = self._build_app_dict(request, app_label)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Сортируйте модели индивидуально в каждом приложении.
    for app in app_list:
        if app['app_label'] == 'wanmark':
            ordering = {
                'SettingsBot': 1,
                'MainMenuBot': 2,
                'SubMenuBot': 3,
                'DoorCardBot': 4,
                'InstallDoorCardBot': 5,
                'NewsletterBot': 6,
            }
            app['models'].sort(key=lambda x: ordering[x['object_name']])

    return app_list


admin.AdminSite.get_app_list = get_app_list
