from django.core.cache import cache
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .forms import MailRecipientForm, MessageForm, MailingForm
from .models import Mailing, MailingAttempt
from web_app.services import MailingAttemptService
from django.views.decorators.cache import cache_page

from web_app.models import MailRecipient, Message
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class OwnerRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки, является ли пользователь владельцем объекта"""

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        if user == obj.owner:
            return True
        if (
            user.has_perm("your_app.can_disable_mailing")
            and self.request.resolver_match.url_name == "mailing_update"
        ):
            return True
        return False


class BaseView(TemplateView):
    template_name = "web_app/base.html"


class MainView(TemplateView):
    template_name = "web_app/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        # 1. Общее количество всех созданных рассылок
        context["total_mailings"] = Mailing.objects.count()

        # 2. Количество активных рассылок
        # Условие: start_time <= now <= end_time И статус 'started'
        context["active_mailings"] = Mailing.objects.filter(
            start_time__lte=now, end_time__gte=now, status="started"
        ).count()

        # 3. Количество уникальных получателей
        context["unique_recipients"] = MailRecipient.objects.distinct().count()

        return context


@method_decorator(cache_page(60 * 15), name="dispatch")
class MailRecipientListView(LoginRequiredMixin, ListView):
    model = MailRecipient

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.has_perm("your_app.can_view_any_mailing"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


@method_decorator(cache_page(60 * 15), name="dispatch")
class MailRecipientDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = MailRecipient

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class MailRecipientCreateView(LoginRequiredMixin, OwnerRequiredMixin, CreateView):
    model = MailRecipient
    form_class = MailRecipientForm
    success_url = reverse_lazy("web_app:recipient_list")


class MailRecipientUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = MailRecipient
    form_class = MailRecipientForm
    success_url = reverse_lazy("web_app:recipient_list")

    def get_success_url(self):
        return reverse("web_app:recipient_detail", args=[self.kwargs.get("pk")])


class MailRecipientDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = MailRecipient
    success_url = reverse_lazy("web_app:message_list")


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageListView(LoginRequiredMixin, ListView):
    model = Message


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.save()
        return self.object


class MessageCreateView(LoginRequiredMixin, OwnerRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("web_app:message_list")


class MessageUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("web_app:message_list")

    def get_success_url(self):
        return reverse("web_app:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("web_app:message_list")


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        user = self.request.user
        cache_key = f"mailings_list_user_{user.id}_{user.is_staff}"
        queryset = cache.get(cache_key)

        if queryset is None:
            if user.is_staff or user.has_perm("your_app.can_view_any_mailing"):
                queryset = Mailing.objects.all()
            else:
                queryset = Mailing.objects.filter(owner=user)

            cache.set(cache_key, queryset, 900)

        return queryset


@method_decorator(cache_page(60 * 15), name="dispatch")
class MailingDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attempts"] = self.object.attempts.all().order_by("-attempt_time")
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(LoginRequiredMixin, OwnerRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("web_app:mailing_list")


class MailingUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("web_app:mailing_list")

    def get_success_url(self):
        return reverse("web_app:mailing_detail", args=[self.kwargs.get("pk")])


class MailingDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("web_app:mailing_list")


@method_decorator(cache_page(60 * 15), name="dispatch")
class MailingStartView(LoginRequiredMixin, OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=kwargs.get("pk"))

        success, message = MailingAttemptService.send_mailing(mailing)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect("web_app:mailing_detail", pk=mailing.pk)


@method_decorator(cache_page(60 * 15), name="dispatch")
class MailingAttemptListView(LoginRequiredMixin, OwnerRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "web_app/mailing_attempt_list.html"
    context_object_name = "attempts"  # удобное имя для цикла в шаблоне

    def get_queryset(self):
        # Ограничиваем вывод последними 50 записями
        return MailingAttempt.objects.all().order_by("-attempt_time")[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Считаем общую статистику по всем логам (не только по последним 50)
        all_attempts = MailingAttempt.objects.all()

        context["total_count"] = all_attempts.count()
        context["success_count"] = all_attempts.filter(status="Успешно").count()
        context["failed_count"] = all_attempts.filter(status="Не успешно").count()

        return context
