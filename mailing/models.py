from django.db import models
from django.utils import timezone


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")

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

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings')
    recipients = models.ManyToManyField(Recipient, related_name='mailings')
    first_sent_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField()

    # Поле статуса из базы данных (оставляем для истории и фильтров в админке)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    @property
    def actual_status(self):
        """
        Динамическое вычисление статуса на основе текущего времени.
        """
        now = timezone.now()

        # 1. Если время окончания уже прошло -> Завершена
        if now > self.end_at:
            return 'Завершена'

        # 2. Если время не вышло, но письма уже отправлялись -> Запущена
        if self.first_sent_at:
            return 'Запущена'

        # 3. Если ничего не произошло -> Создана
        return 'Создана'

    def __str__(self):
        return f"Рассылка: {self.message.subject}"