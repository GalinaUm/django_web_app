from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import MailRecipientForm


from web_app.models import MailRecipient


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


