
from django.contrib import admin
from django.contrib import messages
from .models import Attempt, Mailing, Message, Recipient
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


class AttemptInline(admin.TabularInline):
    model = Attempt
    extra = 0
    readonly_fields = ('attempt_time', 'recipient', 'status', 'server_response')
    can_delete = False


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('status', 'start_time', 'end_time')
    list_filter = ('status',)
    inlines = [AttemptInline]

    # Подключаем действие.
    # Обратите внимание: для классов-действий используется запись [Класс.__name__]
    # или можно создать функцию-обертку, которая вернет класс.
    actions = [SendMailingAction]


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('attempt_time', 'mailing', 'recipient', 'status')
    list_filter = ('status',)
    readonly_fields = ('attempt_time', 'mailing', 'recipient', 'status', 'server_response')
    search_fields = ('recipient__email', 'mailing__message__subject')