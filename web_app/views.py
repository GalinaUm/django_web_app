from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import MailRecipientForm, MessageForm

from web_app.models import MailRecipient, Message


class BaseView(TemplateView):
    template_name = 'web_app/base.html'


class MainView(TemplateView):
    template_name = 'web_app/main.html'


class MailRecipientListView(ListView):
    model = MailRecipient


class MailRecipientDetailView(DetailView):
    model = MailRecipient

    def get_object(self, queryset = None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class MailRecipientCreateView(CreateView):
    model = MailRecipient
    form_class = MailRecipientForm
    success_url = reverse_lazy('MailRecipientListView')


class MailRecipientUpdateView(UpdateView):
    model = MailRecipient
    form_class = MailRecipientForm
    success_url = reverse_lazy('MailRecipientListView')

    def get_success_url(self):
        return reverse('web_app:recipient_detail', args=[self.kwargs.get('pk')])


class MailRecipientDeleteView(DeleteView):
    model = MailRecipient
    success_url = reverse_lazy('MailRecipientListView')


class MessageListView(ListView):
    model = Message

class MessageDetailView(DetailView):
    model = Message
    def get_object(self, queryset = None):
        self.object = super().get_object(queryset)
        self.object.save()
        return self.object

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('MessageListView')

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('MessageListView')

    def get_success_url(self):
        return reverse('web_app:message_detail', args=[self.kwargs.get('pk')])

class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('MessageListView')


