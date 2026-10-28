from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from gent.forms import GentRegisterForm
from django.core.mail import send_mail
from django.conf import settings

from_email = settings.DEFAULT_FROM_EMAIL

class RegisterView(CreateView):
    template_name = 'registration.html'
    form_class = GentRegisterForm
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)

        send_mail(
            subject="Добро пожаловать в наш сервис",
            message="Спасибо, что зарегистрировались в нашем сервисе!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.object.email],
            fail_silently=False,
        )

        return response