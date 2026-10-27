from django import forms
from django.utils import timezone
from .models import Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'


def clean(self):
    cleaned_data = super().clean()
    start = self.cleaned_data.get('start_time')
    stop = self.cleaned_data.get('end_time')

    if not start or not stop:
        return cleaned_data

    real_time = timezone.now()

    if start > stop:
        self.add_error('start_time', 'Время старта должно быть раньше времени окончания.')

    elif start < real_time:
        self.add_error('start_time', 'Время старта не должно быть в прошлом.')

    elif start is None or stop is None:
        self.add_error('start_time', 'Нужно ввести значение времени.')

    return cleaned_data