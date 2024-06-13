import asyncio

from django.contrib import admin, messages
from django.shortcuts import redirect, reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from bot.main_bot import send_newsletter_bot
from wanmark.forms import SettingsBotAdminForm, InstallDoorCardBotAdminForm
from wanmark.models import MainMenuBot, SubMenuBot, DoorCardBot, ImageTitleDoorCardBot, ImageInstallDoorCardBot, \
    SettingsBot, InstallDoorCardBot, NewsletterBot, ImageNewsletterBot
from wanmark.tasks import send_bot


class DoorCardBotInline(admin.StackedInline):
    model = DoorCardBot
    fields = ["name", "title"]
    extra = 0
    show_change_link = True


class SubMenuBotInline(admin.TabularInline):
    model = SubMenuBot
    fields = ["name", "title"]
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
        if obj.image:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return _('(Нет изображения)')

    image_view.short_description = (_('Предварительный просмотр'))


class ImageInstallDoorCardBotInline(admin.TabularInline):
    model = ImageInstallDoorCardBot
    fields = ['image_view']
    readonly_fields = ['image_view']
    max_num = 0
    extra = 0

    def image_view(self, obj):
        if obj.image:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_view.short_description = (_('Предварительный просмотр'))


class InstallDoorCardBotInline(admin.StackedInline):
    form = InstallDoorCardBotAdminForm
    model = InstallDoorCardBot
    fieldsets = [
        (None, {'fields': [("name", "title")]}),
        (None, {'fields': ["image_view"]}),
    ]
    readonly_fields = ['image_view']
    extra = 0
    show_change_link = True

    @admin.display(description='Предварительный просмотр')
    def image_view(self, obj):
        html = ''
        for image_install in obj.imageinstalldoorcardbot_set.all():
            html += '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(image_install.image.url)
        else:
            if html:
                return mark_safe(html)
            else:
                return _('(Нет изображения)')


@admin.register(InstallDoorCardBot)
class InstallDoorCardBotAdmin(admin.ModelAdmin):
    form = InstallDoorCardBotAdminForm
    list_display = ("name", "title")
    inlines = [ImageInstallDoorCardBotInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_images(form.instance)


@admin.register(DoorCardBot)
class DoorCardBotAdmin(admin.ModelAdmin):
    list_display = ("name", "title")
    inlines = [ImageTitleDoorCardBotInline, InstallDoorCardBotInline]


@admin.register(SettingsBot)
class SettingsBotAdmin(admin.ModelAdmin):
    form = SettingsBotAdminForm
    list_display = ['main_title', 'main_image', 'image_view']
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
        if obj.main_image:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.main_image.url))
        else:
            return _('(Нет изображения)')


class ImageNewsletterBotInline(admin.TabularInline):
    model = ImageNewsletterBot
    fields = ['image', 'image_view']
    readonly_fields = ['image_view']
    extra = 0
    show_change_link = True

    def image_view(self, obj):
        if obj.image:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return _('(Нет изображения)')

    image_view.short_description = (_('Предварительный просмотр'))


@admin.register(NewsletterBot)
class NewsletterBotAdmin(admin.ModelAdmin):
    actions = ['send_newsletter']
    list_display = ("title", "count_all", 'count_delivered', 'status_view', 'send_date', 'create_date')
    fields = ["title"]
    readonly_fields = ["count_all", 'count_delivered', 'status', 'send_date']
    inlines = [ImageNewsletterBotInline]

    def status_view(self, obj):
        if obj.status == 0:
            return mark_safe('<a style="background: #6c757d;padding: 3px 12px;border-radius: 15px;color: #fff">Создана</a>')
        elif obj.status == 1:
            return mark_safe('<a style="background: #ffc107;padding: 3px 12px;border-radius: 15px;">Запущена</a>')
        elif obj.status == 2:
            return mark_safe('<a style="background: #198754;padding: 3px 12px;border-radius: 15px;color: #fff">Завершена</a>')

    status_view.short_description = (_('Статус отправки'))

    @admin.action(description='Отправить рассылку')
    def send_newsletter(self, request, queryset):
        if len(queryset) == 1:
            if queryset[0].status != 0:
                self.message_user(request, f"Нельзя отправить рассылку {queryset[0].id}:'{queryset[0].title}' повторно.",
                                  messages.ERROR)
                return None
            nl: NewsletterBot = NewsletterBot.objects.get(id=queryset[0].id)
            nl.send_date = timezone.now()
            # nl.status = 1
            nl.save()

            send_bot.delay(nl.id)
            # asyncio.run(send_newsletter_bot(nl))
            # asyncio.run(send(nl))
            # loop = asyncio.get_event_loop()
            # asyncio.create_task(send_newsletter_bot(nl))
            # loop = asyncio.get_event_loop()
            # loop.create_task(send_newsletter_bot(nl))
            # await asyncio.gather(loop.create_task(send_newsletter_bot(nl)))
            self.message_user(request, f"Рассылка запущена.", messages.SUCCESS, )
        else:
            self.message_user(request, f"Можно отправить только одну рассылку, а не {len(queryset)}.", messages.ERROR)



