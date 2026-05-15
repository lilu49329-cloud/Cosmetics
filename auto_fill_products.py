import os
import django
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import random
import time
import re
import shutil
import uuid
from decimal import Decimal
from datetime import datetime
from django.conf import settings

# ---------------------------
# ⚙️ Thiết lập Django
# ---------------------------
# ⚠️ Đổi 'cosmetic_shop' thành tên project thật của bạn (thư mục chứa settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

# ---------------------------
# Sau khi setup Django mới import models
# ---------------------------
from products.models import Product, ProductImage
from cosmetic_dictionary import cosmetic_dict, partial_translate, keep_original

# ---------------------------
# Các cấu hình cơ bản
# ---------------------------
translator = Translator()

brand_country_map = {
    "maybelline": "Mỹ",
    "l'oreal": "Pháp",
    "nyx": "Mỹ",
    "clinique": "Mỹ",
    "benefit": "Mỹ",
    "catrice": "Đức",
    "marcelle": "Canada",
    "covergirl": "Mỹ",
    "stila": "Mỹ",
    "carslan": "Trung Quốc",
    "sante": "Đức",
    "revlon": "Mỹ",
    "almay": "Mỹ",
    "milani": "Mỹ",
    "pacifica": "Mỹ",
    "mistura": "Canada"
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# ---------------------------
# 🧠 Hàm dịch thông minh (ưu tiên từ điển)
# ---------------------------
def translate_text(text):
    if not text:
        return ""
    original = text
    text_lower = text.lower()

    for keep in keep_original:
        if keep in text_lower:
            return original

    for eng, vi in cosmetic_dict.items():
        pattern = r"\b" + re.escape(eng) + r"\b"
        text = re.sub(pattern, vi, text, flags=re.IGNORECASE)

    for eng, vi in partial_translate.items():
        if eng in text_lower:
            text = re.sub(rf"(?i){eng}", vi, text)

    eng_ratio = len(re.findall(r"[A-Za-z]", text)) / max(len(text), 1)
    if eng_ratio > 0.4:
        try:
            text = translator.translate(original, dest="vi").text
        except Exception:
            pass

    return text.strip()

# ---------------------------
# 🔍 Hàm tìm kiếm & tải dữ liệu
# ---------------------------
def safe_request(url):
    for _ in range(3):
        try:
            time.sleep(random.uniform(1.5, 3.0))
            res = requests.get(url, headers=HEADERS, timeout=10)
            if res.status_code == 200:
                return res
        except requests.RequestException:
            continue
    return None

def search_google_info(name, brand_name=""):
    query = f"{brand_name} {name} mỹ phẩm chính hãng mô tả"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    res = safe_request(url)
    if not res:
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    snippets = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
    results = [s.get_text() for s in snippets if s.get_text()]
    return results[:5]

def search_google_image(name, brand_name=""):
    query = f"{brand_name} {name} mỹ phẩm chính hãng"
    url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
    res = safe_request(url)
    if not res:
        return None
    soup = BeautifulSoup(res.text, "html.parser")
    imgs = soup.find_all("img")
    for img in imgs:
        src = img.get("src")
        if not src or not src.startswith("http"):
            continue
        if any(x in src.lower() for x in ["logo", "icon", "sample", "clipart"]):
            continue
        try:
            head = requests.head(src, timeout=5)
            if "content-length" in head.headers:
                if int(head.headers["content-length"]) < 10000:
                    continue
        except Exception:
            pass
        return src
    return None

def download_image(product, url, prefix="main"):
    try:
        res = requests.get(url, stream=True, timeout=10)
        if res.status_code == 200:
            ext = url.split(".")[-1].split("?")[0]
            filename = f"{product.id}_{prefix}_{uuid.uuid4().hex[:8]}.{ext}"
            path_dir = os.path.join(settings.MEDIA_ROOT, "images")
            os.makedirs(path_dir, exist_ok=True)
            file_path = os.path.join(path_dir, filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(res.raw, f)
            return f"images/{filename}"
    except Exception:
        pass
    return None

# ---------------------------
# 🧴 Hàm fill sản phẩm
# ---------------------------
def extract_info(results):
    desc, origin, texture = "", "", ""
    for t in results:
        l = t.lower()
        if not desc and any(x in l for x in ["mô tả", "công dụng", "dưỡng da", "son", "phấn", "kem"]):
            desc = t
        if not origin and any(x in l for x in ["xuất xứ", "made in", "sản xuất tại"]):
            origin = t
        if not texture and any(x in l for x in ["kết cấu", "texture", "dạng"]):
            texture = t
    return desc, origin, texture

def fill_missing_fields(product):
    name = product.name
    brand_name = getattr(product.brand, "name", "") if hasattr(product, "brand") else ""
    # print(f"🧴 Đang xử lý: {name}")

    results = search_google_info(name, brand_name)
    desc, origin, texture = extract_info(results)

    product.description = translate_text(product.description or desc or f"{name} giúp dưỡng ẩm, làm đẹp và bảo vệ da hiệu quả.")
    product.texture = translate_text(product.texture or texture or random.choice(["Dạng kem mịn", "Dạng gel nhẹ", "Dạng bột mịn"]))
    product.ingredients = translate_text(product.ingredients or random.choice([
        "Hyaluronic Acid, Niacinamide, Vitamin E, chiết xuất trà xanh",
        "Collagen, Ceramide, chiết xuất thiên nhiên, không chứa paraben"
    ]))
    product.usage = translate_text(product.usage or random.choice([
        "Dưỡng ẩm, làm sáng da, giảm thâm nám, bảo vệ khỏi tia UV",
        "Kiểm soát dầu, ngăn ngừa mụn, phục hồi da tổn thương"
    ]))
    product.how_to_use = translate_text(product.how_to_use or random.choice([
        "Thoa đều lên da sau khi rửa mặt, dùng sáng và tối.",
        "Sử dụng hàng ngày, kết hợp với kem chống nắng."
    ]))
    if hasattr(product, "skin_type"):
        product.skin_type = translate_text(product.skin_type or random.choice([
            "Da dầu", "Da khô", "Da nhạy cảm", "Mọi loại da"
        ]))

    if not product.brand_origin:
        brand_key = brand_name.lower()
        for k, v in brand_country_map.items():
            if k in brand_key:
                product.brand_origin = v
                break
        product.brand_origin = translate_text(product.brand_origin or origin or random.choice(list(brand_country_map.values())))

    if not product.original_price and product.price:
        product.original_price = int(round(float(product.price) * random.uniform(1.1, 1.3), -3))

    # Ảnh chính
    if not product.image:
        img_url = search_google_image(name, brand_name)
        if img_url:
            path = download_image(product, img_url, prefix="main")
            if path:
                product.image = path

    # Ảnh phụ
    if hasattr(product, "productimage_set") and product.productimage_set.count() == 0:
        for i in range(3):
            img_url = search_google_image(f"{brand_name} {name} mỹ phẩm {i}")
            if not img_url:
                continue
            path = download_image(product, img_url, prefix=f"gallery{i}")
            if path:
                ProductImage.objects.create(product=product, image=path)

    # --- Đảm bảo đủ điều kiện bật flash sale ---
    # Điều kiện: có giá gốc > giá hiện tại > 0, có ảnh chính, có mô tả, sản phẩm active, có thương hiệu, xuất xứ, kết cấu, loại da phù hợp
    flash_sale_ready = (
        product.price and product.original_price and product.original_price > product.price and product.price > 0 and
        product.image and product.description and getattr(product, 'is_active', True) and product.brand and product.brand_origin and product.texture and product.skin_type
    )
    # Nếu có trường is_flash_sale_ready hoặc can_flash_sale thì gán
    if hasattr(product, 'is_flash_sale_ready'):
        product.is_flash_sale_ready = flash_sale_ready
    elif hasattr(product, 'can_flash_sale'):
        product.can_flash_sale = flash_sale_ready
    # Nếu có trường flash_sale thì bật flash_sale nếu đủ điều kiện
    if hasattr(product, 'flash_sale') and flash_sale_ready:
        product.flash_sale = True

    product.save()
    # print(f"✅ Đã cập nhật: {name}")

# ---------------------------
# 🚀 Hàm chính
# ---------------------------
def auto_fill_products():
    products = Product.objects.all()
    for p in products:
        fill_missing_fields(p)

if __name__ == "__main__":
    auto_fill_products()
