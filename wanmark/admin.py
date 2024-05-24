from django.contrib import admin
from django.shortcuts import redirect, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from wanmark.models import MainMenuBot, SubMenuBot, DoorCardBot, ImageTitleDoorCardBot, ImageInstallDoorCardBot, \
    SettingsBot


class DoorCardBotInline(admin.StackedInline):
    model = DoorCardBot
    fields = ["name", "title"]

    # optional: make the inline read-only
    # readonly_fields = ["name", "title"]
    # can_delete = False
    # max_num = 0
    extra = 0
    show_change_link = True


class SubMenuBotInline(admin.TabularInline):
    model = SubMenuBot
    fields = ["name", "title"]

    # optional: make the inline read-only
    # readonly_fields = ["name", "title"]
    # can_delete = False
    # max_num = 0
    extra = 0
    show_change_link = True
    inlines = [DoorCardBotInline]


@admin.register(MainMenuBot)
class MainMenuBotAdmin(admin.ModelAdmin):
    list_display = ("name", "title")
    inlines = [SubMenuBotInline, DoorCardBotInline]


@admin.register(SubMenuBot)
class SubMenuBotAdmin(admin.ModelAdmin):
    list_display = ("name", "title")
    inlines = [DoorCardBotInline]


class ImageTitleDoorCardBotInline(admin.TabularInline):
    model = ImageTitleDoorCardBot
    fields = ['image', 'image_view']
    readonly_fields = ['image_view']
    extra = 0
    show_change_link = True

    def image_view(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return (_('(Нет изображения)'))

    image_view.short_description = (_('Предварительный просмотр'))


class ImageInstallDoorCardBotInline(admin.TabularInline):
    model = ImageInstallDoorCardBot
    fields = ["image", 'image_view']
    readonly_fields = ['image_view']
    extra = 0
    show_change_link = True

    def image_view(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_view.short_description = (_('Предварительный просмотр'))


@admin.register(DoorCardBot)
class DoorCardBotAdmin(admin.ModelAdmin):
    list_display = ("name", "title")
    inlines = [ImageTitleDoorCardBotInline, ImageInstallDoorCardBotInline]


@admin.register(SettingsBot)
class SettingsBotAdmin(admin.ModelAdmin):

    list_display = ['main_title', 'main_image', 'image_view']
    # fields = ["title", ("image", "image_view"), 'on_contact', ('contact_button', 'contact_title')]
    fieldsets = [
        ("Настройка описания главного меню", {'fields': ["main_title", ("main_image", "image_view")]}),
        ("Настройка кнопки контакты", {'fields': ['on_contact', ('contact_button', 'contact_title')]}),
        ("Настройка кнопки заявка", {'fields': ['on_application', ('application_button',)]}),
        ("Настройка кнопки рассылка", {'fields': ['on_subscription', ('subscription_button',)]}),
        ("Настройки почтового клиента", {"classes": ["collapse"], "fields": ["on_mail", 'mail_hostname', 'mail_port',
                                                                             'mail_username', 'mail_password',
                                                                             'mail_use_tls', 'mail_email_to'], },),
    ]
    readonly_fields = ['image_view']
    list_max_show_all = 1
    list_per_page = 1
    # form = SettingsBotForm

    def changelist_view(self, request, extra_context=None):
        first_obj = self.model.objects.first()
        if first_obj is not None:
            return redirect(reverse('admin:wanmark_settingsbot_change', args=(first_obj.pk,)))
        return redirect(reverse('admin:wanmark_settingsbot_add'))

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        first_obj = self.model.objects.first()
        if first_obj is not None:
            return redirect(reverse('admin:wanmark_settingsbot_change', args=(first_obj.pk,)))
        return super(SettingsBot, self).add_view(request, form_url, extra_context)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        first_obj = self.model.objects.first()
        if first_obj is not None:
            return False
        return True

    def render_change_form(self, request, context, add=True, change=True, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    @admin.display(description='Предварительный просмотр')
    def image_view(self, obj):
        # ex. the name of column is "image"
        if obj.main_image:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.main_image.url))
        else:
            return '(No image)'
