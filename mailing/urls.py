from django.urls import path
from . import views

# Если тут есть строка app_name = 'mailing', закомментируйте её или удалите
# app_name = 'mailing'

urlpatterns = [
    # Именно эта строка создает имя 'mailing_list'
    path('', views.MailingListView.as_view(), name='mailing_list'),

    path('create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:pk>/edit/', views.MailingUpdateView.as_view(), name='mailing_edit'),
    path('<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/send/', views.SendMailingView.as_view(), name='mailing_send'),
]