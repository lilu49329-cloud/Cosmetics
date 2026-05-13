import os
import django
import sys
import requests
import time
from django.core.files.base import ContentFile

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Product

def get_unsplash_url(name):
    n = name.lower()
    # Broadening keywords
    if any(k in n for k in ['foundation', 'kem nền', 'bb', 'cc', 'cushion']): 
        return 'https://images.unsplash.com/photo-1596704017254-9b121068fb31?w=600'
    if any(k in n for k in ['lipstick', 'son', 'lip', 'tint', 'gloss']): 
        return 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=600'
    if any(k in n for k in ['mascara', 'lash']): 
        return 'https://images.unsplash.com/photo-1631214500115-598fc2cb8d2d?w=600'
    if any(k in n for k in ['eyeliner', 'kẻ mắt', 'eye', 'shadow', 'mắt']): 
        return 'https://images.unsplash.com/photo-1625093742435-6fa192b6fb10?w=600'
    if any(k in n for k in ['powder', 'phấn phủ', 'blush', 'phấn má']): 
        return 'https://images.unsplash.com/photo-1596704017254-9b121068fb31?w=600'
    if any(k in n for k in ['cleanser', 'sữa rửa mặt', 'wash', 'clean', 'tẩy trang', 'micellar']): 
        return 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600'
    if any(k in n for k in ['serum', 'vitamin', 'acid', 'toner', 'nước hoa hồng', 'tonic']): 
        return 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=600'
    if any(k in n for k in ['moisturizer', 'kem dưỡng', 'cream', 'lotion']): 
        return 'https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=600'
    if any(k in n for k in ['sunscreen', 'chống nắng', 'uv', 'sunblock']): 
        return 'https://images.unsplash.com/photo-1552046122-03184de85e08?w=600'
    
    return 'https://images.unsplash.com/photo-1512496011931-d21d88a33502?w=600' # Generic makeup

def fill_images():
    products = Product.objects.filter(image__in=['', None])
    total = products.count()
    if total == 0:
        print("All products have images.")
        return
        
    print(f"Found {total} products without images. Starting fix...")
    
    count = 0
    for p in products:
        img_url = get_unsplash_url(p.name)
        # Add random parameter to avoid cache if possible (though Unsplash urls here are static)
        final_url = f"{img_url}&sig={p.id}"
        
        try:
            resp = requests.get(final_url, timeout=20)
            if resp.status_code == 200:
                p.image.save(f"prod_v2_{p.id}.jpg", ContentFile(resp.content), save=True)
                count += 1
                if count % 5 == 0:
                    print(f"Processed {count}/{total} images...")
            time.sleep(0.5) # Slight delay to be nice to API
        except Exception as e:
            pass

    print(f"Finished. Added {count} images.")

if __name__ == '__main__':
    fill_images()
