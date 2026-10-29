from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from gent.forms import CustomAuthForm
from gent.views import RegisterView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    #path('gentlogin/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailing_start'), name='logout'),


   path('gentlogin/', auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=CustomAuthForm  # <--- Вот сюда передаем форму
    ), name='login'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),

    # 2. Страница "Письмо отправлено"
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    # 3. Страница ввода нового пароля (сюда ведёт ссылка из письма)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # 4. Страница "Пароль успешно изменён"
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]