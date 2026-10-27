from django import forms
from django.db import models
from django.utils import timezone



class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О. строкой")
    comment =models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    # Поле статуса из базы данных (оставляем для истории и фильтров в админке)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    message = models.ForeignKey(
        'Message',
        on_delete=models.CASCADE,
        null=True,  # <--- Разрешаем пустое значение в БД
        blank=True,  # <--- Разрешаем пустое значение в формах
        verbose_name="Сообщение"
    )

    recipients = models.ManyToManyField(
        'Recipient',
        verbose_name="Получатели",
        blank=True) # Разрешаем создавать рассылку без выбора получателей (на этапе теста)

    def update_status(self):
        now = timezone.now()
        if self.start_time is None or self.end_time is None:
            return
        # Логика обновления статуса
        if now < self.start_time:
            new_status = 'created'
        elif self.start_time <= now <= self.end_time:
            new_status = 'started'
        else:
            new_status = 'finished'

        # Если статус изменился, сохраняем в базу
        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

    def __str__(self):
        return f"Рассылка: {self.message.subject}"


