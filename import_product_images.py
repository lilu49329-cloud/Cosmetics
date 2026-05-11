import csv
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Product, ProductImage

CSV_PATH = r'c:\Users\admin\Downloads\Cosmetics\productimage_backup.csv'

def import_product_images():
    with open(CSV_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            product_id = row['product_id']
            image_path = row['image']
            alt_text = row['alt_text']
            uploaded_at = row['uploaded_at']
            # Tìm product theo name (dựa vào id -> lấy name từ products_backup.csv)
            product_name = None
            # Đọc tên sản phẩm từ products_backup.csv
            try:
                with open(r'c:\Users\admin\Downloads\Cosmetics\products_backup.csv', encoding='utf-8') as pf:
                    prod_reader = csv.DictReader(pf)
                    for prod_row in prod_reader:
                        if prod_row['id'] == product_id:
                            product_name = prod_row['name'].strip()
                            break
            except Exception as e:
                print(f"Không đọc được tên sản phẩm id={product_id}: {e}")
                continue
            if not product_name:
                print(f"Không tìm thấy tên sản phẩm cho id={product_id}, bỏ qua ảnh {image_path}")
                continue
            # Tìm product theo name (không phân biệt hoa thường, loại bỏ khoảng trắng thừa)
            try:
                product = Product.objects.get(name__iexact=product_name)
            except Product.DoesNotExist:
                print(f"Không tìm thấy sản phẩm tên='{product_name}', bỏ qua ảnh {image_path}")
                continue
            # Kiểm tra đã tồn tại ảnh này chưa
            if ProductImage.objects.filter(product=product, image=image_path).exists():
                print(f"Đã tồn tại ảnh {image_path} cho sản phẩm '{product_name}', bỏ qua")
                continue
            # Tạo ProductImage
            try:
                img = ProductImage(
                    product=product,
                    image=image_path,
                    alt_text=alt_text,
                    uploaded_at=datetime.strptime(uploaded_at.split('+')[0], '%Y-%m-%d %H:%M:%S.%f') if uploaded_at else None
                )
                img.save()
                count += 1
            except Exception as e:
                print(f"Lỗi với ảnh {image_path}: {e}")
        print(f"Đã import {count} ảnh sản phẩm phụ thành công!")

if __name__ == '__main__':
    import_product_images()
