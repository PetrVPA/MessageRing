from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from .forms import MailingForm
from .models import Mailing, Message, Recipient
from .services import MailingSender



# --- CRUD для Рассылок ---

class StartPageView(TemplateView):
    template_name = 'mailing_start.html'

    def dispatch(self, request, *args, **kwargs):
        # Если пользователь авторизован, отправляем его на рассылки
        if request.user.is_authenticated:
            return redirect('mailing_list')  # или '/mailings/'
        return super().dispatch(request, *args, **kwargs)

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    context_object_name = 'mailings'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Считаем всех получателей в базе
        context['total_recipients'] = Recipient.objects.count()
        return context


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_edit.html'
    #fields = ['message', 'recipients', 'end_at']
    success_url = reverse_lazy('mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_edit.html'
    #fields = ['message', 'recipients', 'end_at']
    success_url = reverse_lazy('mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_delete.html'
    success_url = reverse_lazy('mailing_list')


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'
    context_object_name = 'mailing'




    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # Внутри метода должно быть self.save()
        return obj

class ViewRecipients(ListView):
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'
    ordering = ['email']

class CreateRecipients(CreateView):
    model = Recipient
    template_name = 'recipient_create.html'
    fields = ['email', 'full_name', 'comment']  # Обязательно указываем поля!
    success_url = reverse_lazy('recipient_list')

class EditRecipients(UpdateView):
    model = Recipient
    template_name = 'recipient_update.html'
    fields = ['email', 'full_name', 'comment']  # Обязательно указываем поля!
    success_url = reverse_lazy('recipient_list')

class DeleteRecipients(DeleteView):
    model = Recipient
    template_name = 'recipient_delete.html'
    success_url = reverse_lazy('recipient_list')

class DetailRecipients(DetailView):
    model = Recipient
    template_name = 'recipient_detail.html'
    fields = ['email', 'full_name', 'comment']  # Обязательно указываем поля!
    success_url = reverse_lazy('recipient_list')


class ViewMessage(ListView):
    model = Message
    template_name = 'message_list.html'
    context_object_name = 'recipient_messages'
    ordering = ['subject']

class CreateMessage(CreateView):
    model = Message
    template_name = 'message_create.html'
    fields = ['subject', 'body']  # Обязательно указываем поля!
    success_url = reverse_lazy('message_list')

class EditMessage(UpdateView):
    model = Message
    template_name = 'message_update.html'
    fields = ['subject', 'body']  # Обязательно указываем поля!
    success_url = reverse_lazy('message_list')

class DeleteMessage(DeleteView):
    model = Message
    template_name = 'message_delete.html'
    success_url = reverse_lazy('recipient_list')

class DetailMessage(DetailView):
    model = Message
    template_name = 'message_detail.html'
    fields = ['subject', 'body']  # Обязательно указываем поля!
    success_url = reverse_lazy('recipient_list')


class StartMailing(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        # 1. Меняем статус на "started", чтобы класс MailingSender понял, что можно отправлять
        mailing.status = 'started'
        mailing.save(update_fields=['status'])

        # 2. Запускаем отправку
        sender = MailingSender(mailing)
        success, message = sender.send()

        # 3. Выводим сообщение пользователю
        if success:
            messages.success(request, "Рассылка успешно запущена и завершена!")
        else:
            messages.error(request, f"Ошибка: {message}")

        return redirect('mailing_list')  # Перенаправляем обратно в список

