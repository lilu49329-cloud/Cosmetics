import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Product, Brand, Slider

def get_files(path):
    if not os.path.exists(path): return []
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def absolute_sync():
    print("--- Bat dau dong bo tuyet doi ---")
    p_files = get_files('media/products')
    b_files = get_files('media/brands')
    h_files = get_files('media/hotdeals')

    products = Product.objects.all()
    print(f"Dang xu ly {products.count()} san pham...")
    
    # Reset Flash Sale
    Product.objects.update(is_promotion=False)
    
    for i, p in enumerate(products):
        if p_files:
            p.image = f"products/{random.choice(p_files)}"
        if i < 5:
            p.is_promotion = True
            p.is_active = True
        # print(f"Flash Sale: {p.name}")
        p.save()

    brands = Brand.objects.all()
    print(f"Dang xu ly {brands.count()} thuong hieu...")
    for b in brands:
        if b_files:
            b.logo = f"brands/{random.choice(b_files)}"
            b.save()

    slider = Slider.objects.first()
    if slider and h_files:
        slider.image = f"hotdeals/{random.choice(h_files)}"
        slider.is_active = True
        slider.save()
        print("Da cap nhat Slider")

    print("--- Hoan tat dong bo tuyet doi ---")

if __name__ == "__main__":
    absolute_sync()
