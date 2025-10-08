from django.core.management.base import BaseCommand
from products.models import Product, Brand
from django.db import transaction

class Command(BaseCommand):
    help = 'Chuyển đổi dữ liệu brand text sang id (chuẩn hóa cho migration ForeignKey)' 

    def handle(self, *args, **options):
        with transaction.atomic():
            brand_map = {b.name: b.id for b in Brand.objects.all()}
            updated = 0
            for product in Product.objects.all():
                if product.brand and product.brand in brand_map and not product.brand.isdigit():
                    product.brand = str(brand_map[product.brand])
                    product.save(update_fields=["brand"])
                    updated += 1
            self.stdout.write(self.style.SUCCESS(f'Đã cập nhật {updated} sản phẩm: brand text -> id'))
