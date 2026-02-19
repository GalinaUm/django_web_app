from django.urls import path
from web_app.apps import WebAppConfig
from web_app.models import Message
from web_app.views import MailRecipientListView, MainView, BaseView, MailRecipientDetailView, MailRecipientCreateView, \
    MailRecipientUpdateView, MailRecipientDeleteView, MessageListView, MessageCreateView, MessageDetailView, \
    MessageUpdateView, MessageDeleteView

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
    path('web_app/message/<int:pk>/delete/',MessageDeleteView.as_view(), name='message_delete'),
]