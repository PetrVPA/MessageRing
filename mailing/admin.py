
from django.contrib import admin
from django.contrib import messages
from .models import Mailing, Message, Recipient
from .services import MailingSender  # Импортируем наш класс-сервис


class SendMailingAction:
    """Класс-действие для админки."""

    def __init__(self, modeladmin, request, queryset):
        # Этот метод обязателен для действий в админке
        for mailing in queryset:
            sender = MailingSender(mailing)
            success, message = sender.send()

            # Выводим сообщения пользователю в админке
            if success:
                modeladmin.message_user(request, message, messages.SUCCESS)
            else:
                modeladmin.message_user(request, message, messages.ERROR)

    # Описание для выпадающего списка
    @staticmethod
    def description():
        return "Отправить выбранные рассылки (через класс)"


# Регистрация моделей
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    # --- Берем настройки из верхнего варианта ---
    list_display = ('status', 'start_time', 'end_time')
    list_filter = ('status',)
    actions = [SendMailingAction]  # Ваше действие

    # --- Берем фильтрацию из нижнего варианта ---
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Суперпользователи и менеджеры видят всё
        if request.user.is_superuser or request.user.groups.filter(name='Managers').exists():
            return qs
        # Обычные пользователи видят только своё
        return qs.filter(owner=request.user)