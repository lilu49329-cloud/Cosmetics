from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN') == 'true':
            from products.tasks import start_scheduler
            start_scheduler()
