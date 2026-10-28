from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from gent.views import RegisterView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('gentlogin/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailing_start'), name='logout'),
]