import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Product, Brand

# Danh sách thuật ngữ chuẩn ngành mỹ phẩm (có thể bổ sung thêm)
cosmetic_terms = [
    'Son môi', 'Phấn mắt', 'Mascara', 'Chì kẻ', 'Kem nền', 'Dưỡng da', 'Tẩy trang',
    'Lipstick', 'Foundation', 'Powder', 'Cream', 'Makeup', 'Eye', 'Face', 'Skin', 'Serum'
]

# Danh sách thương hiệu quốc tế nổi tiếng
brand_keywords = [
    'Maybelline', "L'Oreal", 'NYX', 'Clinique', 'Benefit',
    'Catrice', 'Marcelle', 'Covergirl', 'Stila'
]

def is_bad_product_name(name):
    if not name:
        return True
    keywords = ['Son môi', 'Phấn mắt', 'Mascara', 'Chì kẻ', 'Kem nền', 'Dưỡng da', 'Tẩy trang']
    if not any(kw.lower() in name.lower() for kw in keywords):
        return True
    if re.search(r'[^a-zA-ZÀ-ỹ0-9\s]', name):
        return True
    if name and name[0].islower():
        return True
    return False

def is_english(text):
    if not text:
        return False
    english_keywords = [
        'the', 'and', 'with', 'for', 'from', 'to', 'ml', 'oz', 'foundation',
        'powder', 'lipstick', 'cream', 'makeup', 'skin', 'eye', 'face', 'description',
        'price', 'usd', 'sale'
    ]
    count = sum(1 for kw in english_keywords if kw in text.lower())
    ascii_ratio = sum(1 for c in text if ord(c) < 128) / max(1, len(text))
    return count > 2 or ascii_ratio > 0.7

def is_bad_translation(text):
    """Check dịch sai tiếng Việt hoặc thuật ngữ mỹ phẩm"""
    if not text:
        return False
    # Nếu có tên thương hiệu → giữ
    if any(kw.lower() in text.lower() for kw in brand_keywords):
        return False
    # Lọc các từ tiếng Việt (có ký tự >127)
    vietnamese_words = [w for w in re.findall(r'\b\w+\b', text) if any(ord(c) > 127 for c in w)]
    misspelled = [w for w in vietnamese_words if w.lower() not in [t.lower() for t in cosmetic_terms]]
    # Sai nếu >50% từ tiếng Việt không đúng thuật ngữ
    if vietnamese_words and len(misspelled)/len(vietnamese_words) > 0.5:
        return True
    return False

def delete_bad_products():
    count = 0
    products = Product.objects.all()
    
    for product in products:
        if getattr(product, 'is_hot', False):
            continue

        brand_name = getattr(product.brand, 'name', '') if product.brand else ''

        # Kiểm tra brand
        def is_vietnamese(text):
            return any(ord(c) > 127 for c in text)

        def is_number(text):
            return text.isdigit()

        def is_multiword(text):
            return len(text.strip().split()) > 1

        if brand_name and (is_number(brand_name) or is_multiword(brand_name)):
            print(f"Xóa sản phẩm: {product.name} (ID: {product.id}) vì brand không hợp lệ: {brand_name}")
            product.delete()
            count += 1
            try:
                brand_obj = Brand.objects.get(name=brand_name)
                print(f"Xóa thương hiệu: {brand_name} (ID: {brand_obj.id})")
                brand_obj.delete()
            except Brand.DoesNotExist:
                pass
            continue

        if brand_name and is_vietnamese(brand_name):
            print(f"Xóa sản phẩm: {product.name} (ID: {product.id}) vì brand tiếng Việt: {brand_name}")
            product.delete()
            count += 1
            continue

        # Kiểm tra dịch sai thuật ngữ tiếng Việt
        if is_bad_translation(product.name) or is_bad_translation(product.description):
            print(f"Xóa sản phẩm do dịch sai/thuật ngữ không chuẩn: {product.name} (ID: {product.id})")
            product.delete()
            count += 1
            continue

        # Kiểm tra tên/mô tả/giá tiếng Anh hoặc tên sản phẩm xấu
        if is_english(product.description) or is_english(str(product.price)) or is_bad_product_name(product.name):
            if is_bad_product_name(product.name) and not any(kw.lower() in product.name.lower() for kw in brand_keywords):
                print(f"Xóa sản phẩm: {product.name} (ID: {product.id})")
                product.delete()
                count += 1
            elif is_english(product.description) or is_english(str(product.price)):
                print(f"Xóa sản phẩm: {product.name} (ID: {product.id})")
                product.delete()
                count += 1

    print(f"Đã xóa {count} sản phẩm tên, mô tả, giá tiếng Anh hoặc dịch sai (trừ sản phẩm hot)!")

if __name__ == "__main__":
    delete_bad_products()
