from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from gent.models import Gent



class GentRegisterForm(UserCreationForm):
    class Meta:
        model = Gent
        fields = ('email', 'password1', 'password2')


class CustomAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # Проверяем флаг is_active
        if not user.is_active:
            raise forms.ValidationError(
                "Ваш аккаунт заблокирован администратором.",
                code='inactive',
            )
        # Вызываем стандартную проверку Django (если нужно)
        super().confirm_login_allowed(user)