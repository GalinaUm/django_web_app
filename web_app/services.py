from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from web_app.models import MailingAttempt


class MailingAttemptService:

    @staticmethod
    def send_mailing(mailing):
        now = timezone.now()

        # 1. Проверка временного интервала
        if not (mailing.start_time <= now <= mailing.end_time):
            return False, "Рассылка недоступна по времени."

        # 2. Подготовка данных
        recipients = mailing.recipients.all()
        count_recipients = len(recipients)  # Считаем количество для статистики
        message = mailing.message

        success_count = 0

        # 3. Цикл отправки
        for recipient in recipients:
            try:
                send_mail(
                    subject=message.subject,
                    message=message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                status = 'Успешно'
                response = f'Email sent to {recipient.email}'
                success_count += 1
            except Exception as e:
                status = 'Не успешно'
                response = f'Error for {recipient.email}: {str(e)}'

            # 4. Запись лога для каждого получателя
            MailingAttempt.objects.create(
                mailing=mailing,
                status=status,
                server_response=response
            )

        # Обновляем статус рассылки (например, на "Выполнена")
        mailing.update_status()

        return True, f"Отправлено {success_count} из {count_recipients} сообщений."
