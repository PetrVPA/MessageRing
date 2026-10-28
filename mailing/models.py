from django import forms
from django.db import models
from django.utils import timezone

from django.conf import settings


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О. строкой")
    comment =models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field='email',
        verbose_name='Владелец',
        related_name='recipients',  # <-- Уникальное имя
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field='email',
        verbose_name='Владелец',
        related_name='messages',  # <-- Оставляем так
        null=True,
        blank=True
    )

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

    @property
    def is_active_now(self):
        """Можно ли запускать рассылку прямо сейчас."""
        now = timezone.now()
        return bool(
            self.start_time
            and self.end_time
            and self.start_time <= now <= self.end_time
        )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field='email',
        verbose_name='Владелец',
        related_name='mailings',  # <-- Уникальное имя
        null=True,
        blank=True
    )


    def __str__(self):
        if not self.message_id:
            return f"Рассылка #{self.pk}"
        return f"Рассылка: {self.message.subject}"


class Attempt(models.Model):
    """История попыток отправки писем по рассылке."""

    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAILED, 'Не успешно'),
    ]

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Рассылка',
    )
    recipient = models.ForeignKey(
        Recipient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attempts',
        verbose_name='Получатель',
    )
    attempt_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время попытки',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Статус',
    )
    server_response = models.TextField(
        blank=True,
        verbose_name='Ответ почтового сервера',
    )

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
        ordering = ['-attempt_time']

    def __str__(self):
        return f"{self.mailing} — {self.get_status_display()}"