from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Mailing, Message, Recipient
from .services import MailingSender


# --- CRUD для Рассылок ---

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    context_object_name = 'mailings'
    ordering = ['-id']

    #def get_queryset(self):
     #   queryset = super().get_queryset()
        # Обновляем статусы перед выводом (костыль, но для учебного проекта сойдет)
     #   for mailing in queryset:
     #       mailing.update_status()
     #   return queryset

class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailing_form.html'
    # Поля, которые пользователь заполняет вручную.
    # Статус и first_sent_at система поставит сама.
    fields = ['message', 'recipients', 'end_at']
    success_url = reverse_lazy('mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing_form.html'
    fields = ['message', 'recipients', 'end_at']
    success_url = reverse_lazy('mailing_list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'
    context_object_name = 'mailing'


class SendMailingView(View):
    def post(self, request, pk):
        # 1. Находим рассылку по ID (pk), переданному в URL
        mailing = get_object_or_404(Mailing, pk=pk)

        # 2. Вызываем наш сервисный класс для отправки
        sender = MailingSender(mailing)
        success, message = sender.send()

        # 3. Добавляем сообщение об успехе или ошибке
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        # 4. Перенаправляем обратно на страницу деталей этой рассылки
        return redirect('mailing_detail', pk=mailing.pk)