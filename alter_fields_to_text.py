
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()
from django.db import connection

def alter_all_fields_to_text():
    sqls = [
        "ALTER TABLE products_product ALTER COLUMN name TYPE text;",
        "ALTER TABLE products_orderitem ALTER COLUMN product_name TYPE text;",
        "ALTER TABLE products_brand ALTER COLUMN name TYPE text;",
        "ALTER TABLE products_promotion ALTER COLUMN name TYPE text;",
        "ALTER TABLE products_category ALTER COLUMN name TYPE text;",
        "ALTER TABLE products_store ALTER COLUMN name TYPE text;",
        "ALTER TABLE products_customer ALTER COLUMN full_name TYPE text;"
    ]
    with connection.cursor() as cursor:
        for sql in sqls:
            cursor.execute(sql)
    print("Đã chuyển tất cả các trường sang kiểu text!")

if __name__ == "__main__":
    alter_all_fields_to_text()
