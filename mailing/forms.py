from django import forms
from django.utils import timezone
from .models import Mailing, Recipient, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Забираем пользователя, которого передадим из views.py
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Фильтруем выпадающий список сообщений
        if user is not None and 'message' in self.fields:
            self.fields['message'].queryset = Message.objects.filter(owner=user)

        # Если у вас в этой же форме есть поле recipients, можно отфильтровать и его:
        if user is not None and 'recipients' in self.fields:
            self.fields['recipients'].queryset = Recipient.objects.filter(owner=user)


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