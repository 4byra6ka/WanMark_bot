from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from users.forms import UserChangeForm, UserCreationForm
from users.models import User

admin.site.unregister(Group)


class EmployeeAdmin(UserAdmin):
    actions = ['gen_passwort_user']
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ['last_login', 'date_joined']
    list_display = ['username', 'first_name', 'last_name', 'last_login']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'telegram')}),
        ('Информация', {'fields': ('first_name', 'last_name',)}),
        ('Разрешения', {'fields': ('is_staff', 'is_superuser',)}),
        ("Расширенные настройки прав доступа", {"classes": ["collapse"], "fields": ["user_permissions"], },),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["username", 'password1', 'password2'], },),
    ]
    ordering = ['username', ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
        content_wanmark = ContentType.objects.filter(app_label='wanmark')
        for content in content_wanmark:
            perms = Permission.objects.filter(content_type=content)
            [obj.user_permissions.add(perm) for perm in perms]

    @admin.action(description='Сброс пароля')
    def gen_passwort_user(self, request, queryset):
        text = ''
        for employee in queryset:
            password = User.objects.make_random_password(
                length=8,
                allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789#_=():,."
            )
            employee.set_password(password)
            employee.save()
            text += f'(логин: {employee.username} пароль: {password} ) '
        self.message_user(request, f"Пароль сброшен на {text}.", messages.SUCCESS,)


admin.site.register(User, EmployeeAdmin)
