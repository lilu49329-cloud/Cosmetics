import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Category, Brand, Product, Slider, Store

def seed_basic_data():
    print("--- Dang khoi tao du lieu mau ---")
    
    # 1. Danh muc
    categories = ["Trang điểm", "Chăm sóc da", "Nước hoa", "Chăm sóc tóc", "Dụng cụ làm đẹp"]
    cat_objs = []
    for cat_name in categories:
        cat, created = Category.objects.get_or_create(name=cat_name)
        cat_objs.append(cat)
        if created: print(f"OK - Da tao danh muc: {cat_name}")

    # 2. Thuong hieu
    brands = ["Maybelline", "L'Oreal", "Carslan", "Innisfree", "La Roche-Posay"]
    brand_objs = []
    for b_name in brands:
        brand, created = Brand.objects.get_or_create(name=b_name)
        brand_objs.append(brand)
        if created: print(f"OK - Da tao thuong hieu: {b_name}")

    # 3. San pham mau (de auto_fill co cai ma chay)
    sample_products = [
        {"name": "Son Kem Lì Maybelline Superstay Vinyl Ink", "brand": brand_objs[0], "category": cat_objs[0], "price": 250000},
        {"name": "Kem Nền L'Oreal Paris Infallible 24h Fresh Wear", "brand": brand_objs[1], "category": cat_objs[0], "price": 320000},
        {"name": "Phấn Phủ Carslan Kiềm Dầu", "brand": brand_objs[2], "category": cat_objs[0], "price": 180000},
        {"name": "Sữa Rửa Mặt La Roche-Posay Effaclar", "brand": brand_objs[4], "category": cat_objs[1], "price": 450000},
    ]

    for p_data in sample_products:
        p, created = Product.objects.get_or_create(
            name=p_data["name"],
            defaults={
                "brand": p_data["brand"],
                "category": p_data["category"],
                "price": p_data["price"],
                "original_price": p_data["price"] + 50000,
                "is_active": True,
                "is_hot": True,
                "is_promotion": True,
                "sale_end": timezone.now() + timedelta(days=7),
                "skin_type": "Mọi loại da",
                "texture": "Dạng kem"
            }
        )
        if created: print(f"OK - Da tao san pham: {p.name}")

    # 4. Slider (de trang chu khong bi trang)
    if Slider.objects.count() == 0:
        Slider.objects.create(
            title="Chào mừng đến với Cosmetics",
            description="Khám phá thế giới mỹ phẩm chính hãng",
            is_active=True
        )
        print("OK - Da tao Slider mac dinh")

    # 5. Cua hang
    if Store.objects.count() == 0:
        Store.objects.create(name="Cosmetics Hà Đông", address="Hà Đông, Hà Nội", phone="0123456789")
        print("OK - Da tao Cua hang mau")

    print("--- Hoan tat seeding co ban ---")

if __name__ == "__main__":
    seed_basic_data()
