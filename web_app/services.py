from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

from web_app.models import MailingAttempt

class MailingAttemptService:

    @staticmethod
    def send_mailing(mailing):
        now = timezone.now()

        if not (mailing.start_time <= now <= mailing.end_time):
            return False, "Рассылка недоступна по времени."

        recipients = mailing.recipients.all()
        message = mailing.message

        for recipient in recipients:
            try:
                send_mail(
                    subject=message.subject,
                    message=message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='Успешно',
                    server_response='Email sent successfully',
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='Не успешно',
                    server_response=str(e),
                )

        mailing.update_status()
        return True, "Рассылка успешно выполнена."



