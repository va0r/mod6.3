from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingSettingsCreateView, MailingSettingsUpdateView, ClientListView, \
    ClientCreateView, ClientUpdateView, ClientDeleteView, MailingSettingsDeleteView, MessageListView, MessageDeleteView, \
    MessageUpdateView, MessageCreateView, MailingSettingsListView, toggle__is_blocked, ContactListView

app_name = MailingConfig.name

urlpatterns = [
    path('', MailingSettingsListView.as_view(), name='mailing_list'),
    path('create/', MailingSettingsCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='mailing_delete'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='clients_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='clients_delete'),

    path('clients/toggle/<int:pk>/', toggle__is_blocked, name='client__is_blocked_toggle'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='messages_create'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='messages_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='messages_delete'),

    path('contacts/', ContactListView.as_view(), name='contacts'),
]
