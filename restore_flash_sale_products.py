import os
import django
import csv

# === Thiết lập Django ===
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Product, Category, Brand

# === Đường dẫn file CSV ===
BACKUP_PATH = r'c:\Users\admin\Downloads\Cosmetics\products_backup.csv'


# === Khôi phục sản phẩm 1 và 3 ===
def restore_flash_sale_products():
    print("🚀 Bắt đầu khôi phục sản phẩm 1 và 3...")

    with open(BACKUP_PATH, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["id"] not in ["2"]:
                continue

            name = row["name"].strip()
            brand_name = row["brand"].strip()
            description = row.get("description", "").strip()

            brand, _ = Brand.objects.get_or_create(name=brand_name)

            category_id = row.get("category_id")
            category = Category.objects.filter(id=category_id).first() if category_id else None
            if not category:
                category, _ = Category.objects.get_or_create(name="Trang điểm")

            price = int(row["price"]) if row["price"] else 0
            quantity = int(row["quantity_in_stock"]) if row["quantity_in_stock"] else 0
            image = row.get("image", "")
            is_active = row.get("is_active", "").lower() in ["true", "t", "1"]

            if Product.objects.filter(name=name, brand=brand, category=category).exists():
                print(f"⚠️ Sản phẩm đã tồn tại: {name}")
                continue

            product = Product(
                name=name,
                brand=brand,
                category=category,
                description=description,
                price=price,
                quantity_in_stock=quantity,
                is_active=is_active,
            )
            if image:
                product.image = image

            product.save()
            print(f"✅ Đã khôi phục sản phẩm: {name}")

    print("🎯 Hoàn tất khôi phục sản phẩm 1 và 3!")


if __name__ == "__main__":
    restore_flash_sale_products()
