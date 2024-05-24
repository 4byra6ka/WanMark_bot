from django import forms


class SettingsBotAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'mail_password': forms.PasswordInput(render_value=True),
        }
