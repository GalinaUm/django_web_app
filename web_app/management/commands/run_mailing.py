from django.core.management.base import BaseCommand
from web_app.models import Mailing
from web_app.services import MailingAttemptService

class Command(BaseCommand):
    help = 'Запуск конкретной рассылки по ID'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int)

    def handle(self, *args, **options):
        try:
            mailing = Mailing.objects.get(pk=options['mailing_id'])
            success, message = MailingAttemptService.send_mailing(mailing)
            if success:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.ERROR(message))
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR('Рассылка не найдена'))
