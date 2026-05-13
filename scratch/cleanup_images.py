import os
import django
import sys
from PIL import Image

# Setup UTF-8 encoding for stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Product

import hashlib

def get_image_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def cleanup_images():
    products = Product.objects.all()
    count_deleted = 0
    count_duplicates = 0
    
    seen_hashes = {} # hash -> product_id
    
    BAD_KEYWORDS = [
        'logo', 'icon', 'banner', 'avatar', 'profile', 'placeholder', 
        'no-image', 'default', 'transparent', 'brand', 'clothing', 
        'mewarnai', 'kartini', 'trang-phuc', 'fruit', 'animal', 'map',
        'cartoon', 'vector', 'illustration', 'nature', 'food', 'vegetable',
        'flower', 'tree', 'landscape', 'person', 'human', 'dress', 'shoe',
        'toy', 'game', 'car', 'building', 'house', 'furniture', 'interior',
        'exterior', 'diagram', 'chart', 'graph', 'text', 'quote', 'meme',
        'art', 'drawing', 'painting', 'sketch', 'hoa-qua', 'trai-cay',
        'con-vat', 'dong-vat', 'hoat-hinh', 'ban-do', 'thuc-an', 'mon-an',
        'quan-ao', 'vay', 'giay', 'do-choi', 'xe-co', 'nha-cua', 'staticmap',
        'googlemaps', 'location', 'gps', 'streetview', 'village', 'african',
        'watch', 'apple', 'iphone', 'macbook', 'gadget', 'tech', 'electronics',
        'news', 'article', 'story', 'coal', 'mine', 'cow', 'methane', 'violence',
        'gun', 'rapper', 'youtube', 'thumbnail', 'ytimg', 'freepik', 'vector',
        'background', 'wallpaper'
    ]
    
    print(f"Checking images for {products.count()} products...")
    
    for product in products:
        if not product.image:
            continue
            
        img_path = product.image.path
        if not os.path.exists(img_path):
            continue
            
        should_delete = False
        reason = ""
        
        # 1. Duplicate detection (Hash)
        img_hash = get_image_hash(img_path)
        if img_hash in seen_hashes:
            should_delete = True
            reason = f"Duplicate image (Same as Product {seen_hashes[img_hash]})"
            count_duplicates += 1
        else:
            seen_hashes[img_hash] = product.id

        # 2. Check file size
        if not should_delete:
            size_kb = os.path.getsize(img_path) / 1024
            if size_kb < 12:
                should_delete = True
                reason = f"Small size ({size_kb:.1f} KB)"
            
        # 3. Check filename keywords (whole word or specific patterns)
        if not should_delete:
            filename_lower = os.path.basename(img_path).lower()
            words = filename_lower.replace('_', ' ').replace('-', ' ').replace('.', ' ').split()
            for kw in BAD_KEYWORDS:
                if kw in words:
                    should_delete = True
                    reason = f"Keyword match: {kw}"
                    break
            
            if not should_delete:
                for special in ['map', 'cartoon', 'illustration', 'vector', 'fruit', 'animal']:
                    if special in filename_lower and special not in product.name.lower():
                        should_delete = True
                        reason = f"Special keyword match: {special}"
                        break
        
        # 4. Check dimensions, aspect ratio and lightness/background
        if not should_delete:
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    if width < 250 or height < 250:
                        should_delete = True
                        reason = f"Small dimensions ({width}x{height})"
                    elif width / height > 2.5 or height / width > 2.5:
                        should_delete = True
                        reason = f"Bad aspect ratio ({width/height:.1f})"
                    else:
                        small_img = img.resize((50, 50)).convert('RGB')
                        pixels = list(small_img.getdata())
                        light_pixels = sum(1 for r, g, b in pixels if r > 220 and g > 220 and b > 220)
                        light_ratio = light_pixels / len(pixels)
                        
                        if light_ratio < 0.15:
                            green_pixels = sum(1 for r, g, b in pixels if g > r + 20 and g > b + 20)
                            if green_pixels / len(pixels) > 0.2:
                                should_delete = True
                                reason = f"Likely nature/landscape (Green ratio: {green_pixels/len(pixels):.2f})"
                            else:
                                should_delete = True
                                reason = f"Low background lightness ({light_ratio:.2f})"
            except Exception as e:
                should_delete = True
                reason = f"Error opening image: {e}"

        if should_delete:
            print(f"Deleting image for product {product.id} ({product.name}): {reason}")
            # Clear the field
            product.image = None
            product.save()
            count_deleted += 1

    print(f"\nCleanup finished. Deleted {count_deleted} images ({count_duplicates} were duplicates).")

if __name__ == "__main__":
    cleanup_images()

if __name__ == "__main__":
    cleanup_images()
