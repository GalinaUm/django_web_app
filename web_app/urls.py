from django.urls import path
from web_app.apps import WebAppConfig
from web_app.views import MainView, BaseView, MailRecipientListView, MailRecipientDetailView, MailRecipientCreateView, \
    MailRecipientUpdateView, MailRecipientDeleteView, MessageListView, MessageCreateView, MessageDetailView, \
    MessageUpdateView, MessageDeleteView, MailingListView, MailingDeleteView, MailingUpdateView, MailingDetailView, \
    MailingCreateView

app_name = WebAppConfig.name


urlpatterns = [
    path('web_app/main/', MainView.as_view(), name='main'),
    path('web_app/base/', BaseView.as_view(), name='base'),
    path('web_app/recipient_list/', MailRecipientListView.as_view(), name='recipient_list'),
    path('web_app/create/', MailRecipientCreateView.as_view(), name='recipient_create'),
    path('web_app/<int:pk>/', MailRecipientDetailView.as_view(), name='recipient_detail'),
    path('web_app/<int:pk>/update/', MailRecipientUpdateView.as_view(), name='recipient_update'),
    path('web_app/<int:pk>/delete/', MailRecipientDeleteView.as_view(), name='recipient_delete'),
    path('web_app/message_list/', MessageListView.as_view(), name='message_list'),
    path('web_app/message_create/', MessageCreateView.as_view(), name='message_create'),
    path('web_app/message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('web_app/message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('web_app/message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('web_app/mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('web_app/mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('web_app/mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('web_app/mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('web_app/mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]