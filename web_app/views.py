from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .forms import MailRecipientForm, MessageForm, MailingForm
from .models import Mailing
from web_app.services import MailingAttemptService

from web_app.models import MailRecipient, Message



class BaseView(TemplateView):
    template_name = 'web_app/base.html'


class MainView(TemplateView):
    template_name = 'web_app/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        # 1. Общее количество всех созданных рассылок
        context['total_mailings'] = Mailing.objects.count()

        # 2. Количество активных рассылок
        # Условие: start_time <= now <= end_time И статус 'started'
        context['active_mailings'] = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status='started'
        ).count()

        # 3. Количество уникальных получателей
        context['unique_recipients'] = MailRecipient.objects.distinct().count()

        return context


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
    success_url = reverse_lazy('web_app:recipient_list')


class MailRecipientUpdateView(UpdateView):
    model = MailRecipient
    form_class = MailRecipientForm
    success_url = reverse_lazy('web_app:recipient_list')

    def get_success_url(self):
        return reverse('web_app:recipient_detail', args=[self.kwargs.get('pk')])


class MailRecipientDeleteView(DeleteView):
    model = MailRecipient
    success_url = reverse_lazy('web_app:message_list')


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
    success_url = reverse_lazy('web_app:message_list')

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('web_app:message_list')

    def get_success_url(self):
        return reverse('web_app:message_detail', args=[self.kwargs.get('pk')])

class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('web_app:message_list')


class MailingListView(ListView):
    model = Mailing

class MailingDetailView(DetailView):
    model = Mailing

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('web_app:mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('web_app:mailing_list')

    def get_success_url(self):
        return reverse('web_app:mailing_detail', args=[self.kwargs.get('pk')])

class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('web_app:mailing_list')


class MailingStartView(View):

    @staticmethod
    def get(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=kwargs.get('pk'))

        success, message = MailingAttemptService.send_mailing(mailing)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect('web_app:mailing_detail', pk=mailing.pk)