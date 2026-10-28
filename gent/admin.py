from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mailing.models import Mailing
from .models import Gent


@admin.action(description='Заблокировать выбранных пользователей')
def block_users(modeladmin, request, queryset):
    # Обновляем статус is_active на False
    queryset.update(is_active=False)

@admin.register(Gent)
class GentAdmin(UserAdmin):
    # Настройки для отображения в списке
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    actions = [block_users]

    # Настройки для формы редактирования
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone', 'state', 'avatar')}),  # Ваши поля
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Настройки для формы создания
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)



