from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext as _

from wanmark.models import InstallDoorCardBot, ImageInstallDoorCardBot


class SettingsBotAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'mail_password': forms.PasswordInput(render_value=True),
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class InstallDoorCardBotAdminForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Описание", required=False)
    images = MultipleFileField(label=_("Добавить фотографии"), required=False)

    class Meta:
        model = InstallDoorCardBot
        fields = ('name', "title", 'images')

    def clean_images(self):
        """Проверка, что можно загружать только изображения."""
        try:
            for upload in self.files.getlist("images"):
                validate_image_file_extension(upload)
        except BaseException:
            pass

    def save_images(self, link_install_door_card):
        """Процесс загрузки фотографии."""
        try:
            for upload in self.files.getlist("images"):
                image = ImageInstallDoorCardBot(link_install_door_card=link_install_door_card, image=upload)
                image.save()
        except BaseException:
            pass
