
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
    list_display = ('message', 'actual_status', 'first_sent_at', 'end_at')
    list_filter = ('status',)

    # Подключаем действие.
    # Обратите внимание: для классов-действий используется запись [Класс.__name__]
    # или можно создать функцию-обертку, которая вернет класс.
    actions = [SendMailingAction]