from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'WanMark'
admin.site.index_title = 'Сайт для администрирования бота'
admin.site.site_title = ''

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),
                  path('', include('users.urls', namespace='users')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    # Retrieve the original list
    app_dict = self._build_app_dict(request, app_label)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Sort the models customably within each app.
    for app in app_list:
        if app['app_label'] == 'wanmark':
            ordering = {
                'SettingsBot': 1,
                'MainMenuBot': 2,
                'SubMenuBot': 3,
                'DoorCardBot': 4
            }
            app['models'].sort(key=lambda x: ordering[x['object_name']])

    return app_list


admin.AdminSite.get_app_list = get_app_list
