from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        import os
        import sys
        # Không chạy scheduler khi đang migrate hoặc chạy lệnh quản lý khác
        if os.environ.get('RUN_MAIN') == 'true' and 'manage.py' in sys.argv and 'runserver' in sys.argv:
            from products.tasks import start_scheduler
            start_scheduler()
