import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Brand

def is_vietnamese(text):
    # Nếu có ký tự tiếng Việt (dấu hoặc ký tự unicode ngoài ASCII)
    return any(ord(c) > 127 for c in text)

def delete_bad_brands():
    count = 0
    brands = Brand.objects.all()
    for brand in brands:
        def is_number(text):
            return text.isdigit()
        def is_multiword(text):
            return len(text.strip().split()) > 1
        if is_number(brand.name) or is_multiword(brand.name) or is_vietnamese(brand.name):
            print(f"Xóa thương hiệu: {brand.name} (ID: {brand.id})")
            brand.delete()
            count += 1
    print(f"Đã xóa {count} thương hiệu tên là số hoặc nhiều hơn 1 từ!")

if __name__ == "__main__":
    delete_bad_brands()
