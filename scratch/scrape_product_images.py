"""
Script scrape ảnh sản phẩm thật - phiên bản có timeout + xử lý lỗi chắc chắn
"""
import os
import django
import sys
import requests
import random
import time
import signal
from django.core.files.base import ContentFile
from contextlib import suppress

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Product
from ddgs import DDGS

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

SKIP_KEYWORDS = ['logo', 'icon', '.svg', 'favicon', 'transparent', 'png?', 'brand-']

def search_image(brand_name, product_name):
    """Search with strict 8-second total timeout."""
    query = f"{brand_name} {product_name} cosmetic product"
    try:
        # Use a fresh DDGS instance each time, with timeout
        ddgs = DDGS(timeout=8)
        results = list(ddgs.images(query, max_results=5, safesearch="off"))
        urls = []
        for r in results:
            url = r.get('image', '')
            if not url:
                continue
            if any(k in url.lower() for k in SKIP_KEYWORDS):
                continue
            urls.append(url)
        return urls
    except Exception:
        return []

def download_image(url):
    try:
        resp = requests.get(url, timeout=8, headers=HEADERS)
        if resp.status_code == 200 and len(resp.content) > 8000:
            ct = resp.headers.get('Content-Type', '')
            if 'image' in ct and 'svg' not in ct:
                return resp.content
    except:
        pass
    return None

def update_products():
    products = list(Product.objects.all().select_related('brand'))
    total = len(products)
    print(f"Starting image update for {total} products...")

    success = 0
    failed = 0

    for i, p in enumerate(products, 1):
        brand_name = p.brand.name if p.brand else "cosmetics"
        
        candidates = search_image(brand_name, p.name)
        img_data = None
        
        for url in candidates[:3]:
            img_data = download_image(url)
            if img_data:
                break

        if img_data:
            p.image.save(f"real_{p.id}.jpg", ContentFile(img_data), save=True)
            success += 1
        else:
            failed += 1

        if i % 10 == 0:
            print(f"[{i}/{total}] OK={success} FAIL={failed}")
        
        time.sleep(0.8)

    print(f"\nDONE. Updated: {success} | Failed: {failed}")

if __name__ == '__main__':
    update_products()
