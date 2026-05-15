from django.db import connection
from django.utils import timezone

def fix():
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO django_migrations (app, name, applied) VALUES ('products', '0005b_brand_data_migration', %s)", [timezone.now()])
            print("Successfully faked migration 0005b")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
    django.setup()
    fix()
