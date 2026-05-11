import os
import django
import json
import re
import requests
from django.core.files.base import ContentFile

# ====================================================
# ⚙️ 1. Thiết lập Django
# ====================================================
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

# ====================================================
# 🧭 2. Import models
# ====================================================
from products.models import Product, Category, Brand

# ====================================================
# 📚 3. Import từ điển mỹ phẩm
# ====================================================
from cosmetic_dictionary import cosmetic_dict, keep_original

# ====================================================
# 📂 4. Đường dẫn dữ liệu
# ====================================================
DATA_PATH = r'c:\Users\admin\Downloads\archive\makeup_data.json'

# ====================================================
# 🧰 5. Các hàm tiện ích
# ====================================================
def get_or_create_category(name):
    if not name:
        name = "Trang điểm"
    category, _ = Category.objects.get_or_create(name=name)
    return category

def get_or_create_brand(name):
    if not name:
        return None
    name = name[:100]
    brand, _ = Brand.objects.get_or_create(name=name)
    return brand

def convert_usd_to_vnd(usd):
    try:
        usd = float(usd)
        vnd = int(usd * 25000)
        tail = vnd % 1000
        if tail < 500:
            vnd -= tail
        elif tail < 900:
            vnd = vnd - tail + 500
        else:
            vnd = vnd - tail + 900
        return vnd, f"{vnd:,} đ"
    except:
        return 0, "0 đ"

def download_image(url):
    if not url:
        return None, None
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return ContentFile(resp.content), url.split('/')[-1]
    except:
        return None, None
    return None, None

# ====================================================
# 🈯 6. Hàm dịch tên sản phẩm — FINAL PRO + SPECIAL TAG
# ====================================================
def translate_name_to_vi(name_text, brand_name=None):
    if not name_text:
        return ''

    # 🧼 Làm sạch chuỗi
    name_text = re.sub(r'[\(\)\[\]\{\},]', '', name_text)
    name_text = re.sub(r"’", "'", name_text)
    lower_name = name_text.lower().strip()

    # 🪄 Dịch ưu tiên cụm dài từ điển
    sorted_keywords = sorted(cosmetic_dict.keys(), key=len, reverse=True)
    for eng in sorted_keywords:
        pattern = r'\b' + re.escape(eng.lower()) + r'\b'
        if re.search(pattern, lower_name):
            lower_name = re.sub(pattern, cosmetic_dict[eng], lower_name)

    words = lower_name.split()

    # 📌 Danh sách cụm product_type ưu tiên theo độ dài và ngành
    product_priority = [
        "phấn má hồng",
        "phấn phủ",
        "kẻ mắt",
        "chuốt mi",
        "kem nền",
        "son môi",
        "bút kẻ mày",
        "chân mày",
        "son",
        "phấn",
        "kem",
        "mắt",
        "môi",
    ]

    translated_values = [v.lower() for v in cosmetic_dict.values()]
    text_for_match = ' '.join(words)

    # 📍 1. Tìm cụm product_type dài nhất trước
    matched_types = []
    for pt in product_priority:
        pattern = r'\b' + re.escape(pt) + r'\b'
        if re.search(pattern, text_for_match):
            matched_types.append(pt)
            text_for_match = re.sub(pattern, '', text_for_match).strip()

    # Loại bỏ product_type khỏi text
    remaining_tokens = text_for_match.split()

    # 📦 Nhóm ngữ nghĩa
    finish_features = set()
    colors = set()
    marketing_tags = []
    special_tags = []

    # 📌 Danh sách cụm marketing đặc biệt cần đẩy về cuối
    special_marketing_tags = ["bộ sưu tập", "collection", "limited edition", "phiên bản giới hạn"]

    # 📍 2. Xử lý phần còn lại
    for token in remaining_tokens:
        lw = token.lower().strip()
        if not lw:
            continue

        # Thương hiệu giữ nguyên
        if (brand_name and lw == brand_name.lower()) or lw in keep_original:
            marketing_tags.append(token)
            continue

        # Màu & đặc tính
        if lw in translated_values:
            if lw in ["đen", "trắng", "đỏ", "hồng", "xanh", "nâu", "be", "vàng", "bạc"]:
                colors.add(lw)
            else:
                finish_features.add(lw)
            continue

        # Cụm marketing đặc biệt
        if lw in special_marketing_tags:
            special_tags.append(token)
            continue

        # Mặc định: slogan
        marketing_tags.append(token)

    # 📍 3. Ghép kết quả theo thứ tự chuẩn
    final_parts = []

    # Loại sản phẩm
    if matched_types:
        matched_types = sorted(matched_types, key=lambda x: product_priority.index(x))
        product_type_str = matched_types[0].capitalize()
        final_parts.append(product_type_str)

    # Màu
    colors = sorted(list(colors))
    if colors:
        final_parts.append(" - Màu " + ' '.join(c.capitalize() for c in colors))

    # Đặc tính
    finish_features = sorted(list(finish_features))
    if finish_features:
        final_parts.append(" - " + ' - '.join(w.capitalize() for w in finish_features))

    # Marketing tags
    if marketing_tags:
        final_parts.append(' '.join(marketing_tags))

    # Special marketing tags — luôn cuối cùng
    if special_tags:
        final_parts.append(' - ' + ' '.join(tag.capitalize() for tag in special_tags))

    final_text = ' '.join(final_parts)
    final_text = re.sub(r'\s+', ' ', final_text).strip()

    # Viết hoa chữ cái đầu câu
    if final_text:
        final_text = final_text[0].upper() + final_text[1:]

    return final_text

# ====================================================
# 🧾 7. Tách mô tả
# ====================================================
def split_description_and_translate(description_text):
    if not description_text:
        return {'description':'','ingredients':'','usage':'','how_to_use':''}

    text_vi = description_text.strip()
    lower_text = text_vi.lower()

    ing_pos = lower_text.find('thành phần')
    usage_pos = lower_text.find('công dụng')
    how_pos = lower_text.find('cách dùng')

    description = ''
    ingredients = ''
    usage = ''
    how_to_use = ''

    positions = []
    if ing_pos != -1: positions.append(('ingredients', ing_pos))
    if usage_pos != -1: positions.append(('usage', usage_pos))
    if how_pos != -1: positions.append(('how_to_use', how_pos))
    positions.sort(key=lambda x: x[1])

    if not positions:
        description = text_vi
    else:
        for i, (label, start) in enumerate(positions):
            end = positions[i+1][1] if i+1 < len(positions) else len(text_vi)
            segment = text_vi[start:end].strip()
            segment = re.sub(r'(?i)^(thành phần|công dụng|cách dùng)\s*[:\-]?\s*', '', segment).strip()
            if label == 'ingredients':
                ingredients = segment
            elif label == 'usage':
                usage = segment
            elif label == 'how_to_use':
                how_to_use = segment

        first_pos = positions[0][1]
        description = text_vi[:first_pos].strip()

    return {
        'description': description,
        'ingredients': ingredients,
        'usage': usage,
        'how_to_use': how_to_use
    }

# ====================================================
# 📦 8. Import sản phẩm (BỎ QUA brand null)
# ====================================================
def import_products():
    with open(DATA_PATH, encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    for idx, item in enumerate(data):
        raw_name = (item.get('name') or '').strip()
        if not raw_name:
            continue

        # ❌ Bỏ qua nếu brand null hoặc rỗng
        brand_raw = item.get('brand')
        if not brand_raw or str(brand_raw).strip() == '':
            continue
        brand_raw = str(brand_raw).strip()

        name_vi = translate_name_to_vi(raw_name, brand_raw)
        name = ' '.join([w.capitalize() for w in name_vi.split()])[:200]

        has_keyword = any(k.lower() in name.lower() for k in cosmetic_dict.values())
        has_product_type = any(x in name_vi.lower() for x in ["son", "kem", "phấn", "kẻ", "chuốt", "mắt", "môi"])
        if not has_keyword or not has_product_type:
            continue

        if brand_raw and len(brand_raw.split()) > 1:
            continue

        brand = get_or_create_brand(brand_raw)
        category = get_or_create_category(item.get('category',''))

        description_raw = item.get('description','')
        split_result = split_description_and_translate(description_raw)
        description = split_result.get('description','')
        ingredients = split_result.get('ingredients','')
        usage = split_result.get('usage','')
        how_to_use = split_result.get('how_to_use','')

        price_int, price_display = convert_usd_to_vnd(item.get('price',0))
        image_link = item.get('image_link','')
        texture = item.get('texture','')
        skin_type = item.get('skin_type','')

        image_file, image_name = download_image(image_link)
        if not (image_file and image_name):
            continue

        if Product.objects.filter(name=name, brand=brand, category=category).exists():
            continue

        try:
            product = Product(
                name=name,
                brand=brand,
                category=category,
                description=description,
                ingredients=ingredients,
                usage=usage,
                how_to_use=how_to_use,
                price=price_int,
                texture=texture,
                skin_type=skin_type,
                quantity_in_stock=item.get('quantity_in_stock',0),
                is_active=True
            )
            if hasattr(product,'price_display'):
                product.price_display = price_display
            product.image.save(image_name, image_file, save=False)
            product.save()
            count += 1

            # 🆕 In tên gốc & tên sau khi dịch
            print(f"📝 Tên gốc: {raw_name}")
            print(f"✅ Sau khi dịch: {name}")
            print("-" * 50)

        except Exception:
            continue

    print(f'🎉 Tổng cộng {count} sản phẩm đã import thành công!')

# ====================================================
# 🏁 9. Chạy chương trình
# ====================================================
if __name__ == '__main__':
    import_products()
