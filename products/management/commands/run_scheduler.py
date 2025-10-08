from django.core.management.base import BaseCommand
from products.tasks import start_scheduler

class Command(BaseCommand):
    help = 'Chạy scheduler flash sale tự động (không phụ thuộc server web)'  # Tiếng Việt

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Bắt đầu chạy scheduler flash sale...'))
        start_scheduler()
        import time
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Đã dừng scheduler!'))
