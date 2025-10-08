from django.core.management.base import BaseCommand
from django.utils import timezone
from products.models import Product

class Command(BaseCommand):
    help = 'Tự động gỡ flag flash sale cho sản phẩm đã hết hạn'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_products = Product.objects.filter(is_flash_sale=True, sale_end__isnull=False, sale_end__lt=now)
        count = expired_products.update(is_flash_sale=False)
        self.stdout.write(self.style.SUCCESS(f'Đã gỡ flash sale cho {count} sản phẩm hết hạn.'))
