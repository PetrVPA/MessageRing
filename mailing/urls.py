from django.urls import path
from . import views


# Если тут есть строка app_name = 'mailing', закомментируйте её или удалите
# app_name = 'mailing'

urlpatterns = [
    # Именно эта строка создает имя 'mailing_list'
    path('', views.MailingListView.as_view(), name='mailing_list'),
    path('mailing_list', views.MailingListView.as_view(), name='mailing_list'),
    path('create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_detail/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_edit/<int:pk>/', views.MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing_delete/<int:pk>', views.MailingDeleteView.as_view(), name='mailing_delete'),


    path('recipient_list/', views.ViewRecipients.as_view(), name='recipient_list'),
    path('recipient_create/', views.CreateRecipients.as_view(), name='recipient_create'),
    path('recipient_update/<int:pk>/', views.EditRecipients.as_view(), name='recipient_update'),
    path('recipient_delete/<int:pk>/', views.DeleteRecipients.as_view(), name='recipient_delete'),
    path('recipient_detail/<int:pk>/', views.DetailRecipients.as_view(), name='recipient_detail'),

    path('message_list/', views.ViewMessage.as_view(), name='message_list'),
    path('message_create/', views.CreateMessage.as_view(), name='message_create'),
    path('message_update/<int:pk>/', views.EditMessage.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', views.EditMessage.as_view(), name='message_delete'),
    path('message_detail/<int:pk>/', views.DetailMessage.as_view(), name='message_detail'),
]