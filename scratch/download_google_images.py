import os
import django
import sys
import shutil
import logging
from icrawler.builtin import BingImageCrawler
from django.core.files import File

# Setup UTF-8 encoding for stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Product

from PIL import Image
import io

def is_valid_product_image(img_data):
    try:
        img = Image.open(io.BytesIO(img_data))
        width, height = img.size
        # Minimum size for a good product image
        if width < 300 or height < 300:
            return False, f"Too small ({width}x{height})"
        # Aspect ratio should be somewhat square
        ratio = width / height
        if ratio > 2.0 or ratio < 0.5:
            return False, f"Bad aspect ratio ({ratio:.2f})"
            
        # Lightness/Background Check
        small_img = img.resize((50, 50)).convert('RGB')
        pixels = list(small_img.getdata())
        
        # Count "light" pixels (R,G,B > 220)
        light_pixels = sum(1 for r, g, b in pixels if r > 220 and g > 220 and b > 220)
        light_ratio = light_pixels / len(pixels)
        
        # Professional product shots usually have a light/white background
        if light_ratio < 0.15:
            # Check for nature colors
            green_pixels = sum(1 for r, g, b in pixels if g > r + 20 and g > b + 20)
            if green_pixels / len(pixels) > 0.2:
                return False, f"Likely nature/landscape (Green ratio: {green_pixels/len(pixels):.2f})"
            return False, f"Low background lightness ({light_ratio:.2f})"
            
        return True, "OK"
    except Exception as e:
        return False, f"Invalid image: {e}"

import hashlib

def get_image_hash(img_data):
    return hashlib.md5(img_data).hexdigest()

def get_existing_hashes():
    hashes = set()
    for product in Product.objects.all():
        if product.image and os.path.exists(product.image.path):
            with open(product.image.path, 'rb') as f:
                hashes.add(hashlib.md5(f.read()).hexdigest())
    return hashes

def download_product_images():
    # Get products that don't have an image or have one we want to replace
    products = Product.objects.all()
    total = products.count()
    print(f"Starting to download validated and unique images for {total} products...")
    
    # Get existing hashes to avoid duplicates
    existing_hashes = get_existing_hashes()
    
    # Create a temporary directory
    tmp_dir = os.path.join('scratch', 'tmp_images')
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    for i, product in enumerate(products, 1):
        # Skip if already has a validated image
        if product.image and "product_" in product.image.name:
             if os.path.exists(product.image.path):
                 valid, _ = is_valid_product_image(open(product.image.path, 'rb').read())
                 if valid:
                     continue

        brand_name = product.brand.name if product.brand else ""
        query = f"{brand_name} {product.name} cosmetic product photo"
        print(f"[{i}/{total}] Searching for: {query}")
        
        product_tmp_dir = os.path.join(tmp_dir, str(product.id))
        if os.path.exists(product_tmp_dir):
            shutil.rmtree(product_tmp_dir)
        os.makedirs(product_tmp_dir)
            
        logging.getLogger('icrawler').setLevel(logging.ERROR)
        crawler = BingImageCrawler(storage={'root_dir': product_tmp_dir})
        
        try:
            # Search for more results if the first one is invalid
            crawler.crawl(keyword=query, max_num=5, overwrite=True)
            
            files = sorted([f for f in os.listdir(product_tmp_dir) if os.path.isfile(os.path.join(product_tmp_dir, f))])
            saved = False
            for filename_tmp in files:
                img_path = os.path.join(product_tmp_dir, filename_tmp)
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                    
                    # 1. Validation check
                    valid, reason = is_valid_product_image(img_data)
                    if not valid:
                        print(f"   --> Skipped: {filename_tmp} ({reason})")
                        continue
                        
                    # 2. Duplicate check (Hash)
                    img_hash = get_image_hash(img_data)
                    if img_hash in existing_hashes:
                        print(f"   --> Skipped: {filename_tmp} (Duplicate image)")
                        continue
                    
                    # Clean filename
                    clean_name = "".join([c for c in product.name if c.isalnum() or c in (' ', '_', '-')]).strip().replace(' ', '_')
                    save_name = f"product_{product.id}_{clean_name}.jpg"
                    product.image.save(save_name, File(io.BytesIO(img_data)), save=True)
                    
                    # Add to existing hashes to prevent future duplicates in this run
                    existing_hashes.add(img_hash)
                    
                    print(f"   --> Saved: {save_name}")
                    saved = True
                    break
            
            if not saved:
                print(f"   --> No valid images found for {product.name} among 5 results")
                
        except Exception as e:
            print(f"   --> Error crawling for {product.name}: {e}")
        
        shutil.rmtree(product_tmp_dir)

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    print("\nFinished downloading and validating images.")

    # Final Cleanup
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    print("\nFinished downloading all images.")

if __name__ == "__main__":
    download_product_images()
