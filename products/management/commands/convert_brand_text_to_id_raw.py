from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Chuyển đổi dữ liệu brand text sang id trong Product bằng raw SQL (cho PostgreSQL)'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Lấy map tên brand sang id
            cursor.execute("SELECT id, name FROM products_brand")
            brand_map = {name: id for id, name in cursor.fetchall()}
            # Cập nhật từng sản phẩm
            update_count = 0
            for name, id in brand_map.items():
                cursor.execute("""
                    UPDATE products_product
                    SET brand = %s
                    WHERE brand = %s
                """, [str(id), name])
                update_count += cursor.rowcount
        self.stdout.write(self.style.SUCCESS(f'Đã cập nhật {update_count} sản phẩm: brand text -> id (raw SQL)'))
