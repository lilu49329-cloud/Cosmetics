import os
import django
import re
import unicodedata
from googletrans import Translator

# Thiết lập Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cosmetic_shop.settings")
django.setup()

from products.models import Product
from cosmetic_dictionary import cosmetic_dict, partial_translate, keep_original

translator = Translator()

# -------------------------------
# Chuẩn hóa văn bản
# -------------------------------
def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    # Chuẩn hóa các dấu ngoặc và ký tự đặc biệt
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-")
    return text.strip()

# -------------------------------
# Hàm dịch mô tả bằng từ điển + fallback Google Translate
# -------------------------------
def translate_text(text):
    if not text:
        return ""

    text = normalize_text(text)
    lower_text = text.lower()

    # 1. Giữ nguyên thương hiệu hoặc từ khóa không dịch
    for keep in keep_original:
        lower_text = re.sub(
            rf"\b{re.escape(keep.lower())}\b", keep, lower_text, flags=re.IGNORECASE
        )

    # 2. Dịch chính xác từ điển (ưu tiên cụm dài)
    for eng, vi in sorted(cosmetic_dict.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = rf"(?<!\w){re.escape(eng.lower())}(?!\w)"
        lower_text = re.sub(pattern, vi, lower_text, flags=re.IGNORECASE)

    # 3. Dịch bán phần (partial dictionary)
    for eng, vi in partial_translate.items():
        pattern = rf"{re.escape(eng.lower())}"
        lower_text = re.sub(pattern, vi, lower_text, flags=re.IGNORECASE)

    # 4. Fallback Google Translate nếu phát hiện vẫn còn nhiều tiếng Anh
    if re.search(r"[a-zA-Z]{3,}", lower_text):  # nếu vẫn còn tiếng Anh
        try:
            vi_text = translator.translate(lower_text, src="en", dest="vi").text
            lower_text = vi_text
        except Exception:
            pass  # Nếu Google lỗi, giữ nguyên phần đã dịch được

    # 5. Viết hoa chữ cái đầu
    lower_text = lower_text.strip()
    if lower_text:
        lower_text = lower_text[0].upper() + lower_text[1:]

    return lower_text

# -------------------------------
# Hàm tách phần mô tả (desc / ingredients / usage / how_to_use)
# -------------------------------
def split_description(text):
    text = normalize_text(text)
    if not text:
        return {"description": "", "ingredients": "", "usage": "", "how_to_use": ""}

    lower = text.lower()
    parts = {"description": "", "ingredients": "", "usage": "", "how_to_use": ""}

    # Chia mô tả theo từ khóa phổ biến
    if "ingredient" in lower:
        seg = re.split(r"ingredients?:", text, flags=re.IGNORECASE)
        parts["description"] = seg[0]
        if len(seg) > 1:
            rest = seg[1]
            if "usage" in rest.lower() or "how to use" in rest.lower():
                sub = re.split(r"usage:|how to use:", rest, flags=re.IGNORECASE)
                parts["ingredients"] = sub[0]
                if len(sub) > 1:
                    parts["usage"] = sub[1]
            else:
                parts["ingredients"] = rest
    elif "usage" in lower or "how to use" in lower:
        seg = re.split(r"usage:|how to use:", text, flags=re.IGNORECASE)
        parts["description"] = seg[0]
        parts["how_to_use"] = seg[1] if len(seg) > 1 else ""
    else:
        parts["description"] = text

    # Dịch từng phần
    for key in parts:
        parts[key] = translate_text(parts[key])

    return parts

# -------------------------------
# Hàm cập nhật mô tả sản phẩm và hiển thị preview
# -------------------------------
def update_product_descriptions():
    products = Product.objects.filter(description__isnull=False).exclude(description__exact="")
    print(f"🔍 Tìm thấy {products.count()} sản phẩm có mô tả cần dịch...\n")

    updated = 0
    for product in products:
        try:
            result = split_description(product.description)
            product.description = result["description"]
            product.ingredients = result["ingredients"]
            product.usage = result["usage"]
            product.how_to_use = result["how_to_use"]
            product.save()
            updated += 1

            print(f"🟣 {updated}. {product.name}")
            print(f"   📝 Gốc: {normalize_text(product.description)}")
            print(f"   🇻🇳 Dịch: {result['description']}")
            if result['ingredients']:
                print(f"   🌿 Thành phần: {result['ingredients']}")
            if result['usage']:
                print(f"   💧 Công dụng: {result['usage']}")
            if result['how_to_use']:
                print(f"   🪞 Cách dùng: {result['how_to_use']}")
            print("-" * 100)

        except Exception as e:
            print(f"⚠️ Lỗi khi dịch {product.name}: {e}")

    print(f"\n🎯 Hoàn tất! Đã dịch và cập nhật {updated} sản phẩm.\n")

# -------------------------------
# Chạy script
# -------------------------------
if __name__ == "__main__":
    update_product_descriptions()
