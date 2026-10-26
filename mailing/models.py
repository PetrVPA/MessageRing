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
    end_time = models.DateTimeField()
    # Поле статуса из базы данных (оставляем для истории и фильтров в админке)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')


    def __str__(self):
        return f"Рассылка: {self.message.subject}"


