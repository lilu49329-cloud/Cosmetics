
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
import json
from .models import FAQ, ChatHistory, Product, Brand
from django.contrib.auth import get_user_model
import os

def find_faq_by_tags(message, faqs):
    msg = message.lower()
    for f in faqs:
        tags = [t.strip().lower() for t in f.tags.split(',') if t.strip()]
        for tag in tags:
            if tag and (tag in msg or tag in msg.replace('?', '')):
                return f.answer
    return None

def find_faq_by_brand(message, faqs):
    brands = Brand.objects.values_list('name', flat=True)
    for brand in brands:
        if brand.lower() in message.lower():
            for f in faqs:
                if brand.lower() in f.question.lower() or brand.lower() in f.tags.lower():
                    return f.answer
    return None

def find_faq_by_question(message, faqs):
    msg = message.lower().replace('?', '').strip()
    for f in faqs:
        q = f.question.lower().replace('?', '').strip()
        # So khớp toàn bộ hoặc từng từ khóa chính
        if q in msg or msg in q:
            return f.answer
        # So khớp từng từ khóa (nếu câu hỏi dài)
        q_words = set(q.split())
        msg_words = set(msg.split())
        if len(q_words & msg_words) >= max(2, min(len(q_words), len(msg_words)) // 2):
            return f.answer
    return None


def find_product_info(message):
    # Trả lời về tin tức (news)
    if any(kw in msg for kw in ['tin tức', 'news', 'bài viết', 'bài báo', 'sự kiện']):
        # Giả sử có model News với các trường title, summary, created_at
        try:
            from .models import News
            news_list = News.objects.order_by('-created_at')[:5]
            if news_list:
                nlist = '\n'.join([f"- {n.title}: {getattr(n, 'summary', '')[:60]}..." for n in news_list])
                return f"Các tin tức mới nhất của shop:\n{nlist}"
            else:
                return "Hiện chưa có tin tức mới nào."
        except Exception:
            return "Chức năng tin tức chưa được kích hoạt."

    # Trả lời về cửa hàng (store)
    if any(kw in msg for kw in ['cửa hàng', 'store', 'địa chỉ', 'chi nhánh', 'shop ở đâu']):
        # Giả sử có model Store với các trường name, address, phone
        try:
            from .models import Store
            stores = Store.objects.all()
            if stores:
                slist = '\n'.join([f"- {s.name}: {s.address} | SĐT: {getattr(s, 'phone', '')}" for s in stores])
                return f"Danh sách cửa hàng/chi nhánh của shop:\n{slist}"
            else:
                return "Hiện chưa có thông tin cửa hàng."
        except Exception:
            return "Chức năng cửa hàng chưa được kích hoạt."

    # Trả lời về thương hiệu
    if any(kw in msg for kw in ['thương hiệu', 'brand', 'hãng', 'hãng mỹ phẩm']):
        brands = Brand.objects.all()
        if brands:
            blist = ', '.join([b.name for b in brands])
            return f"Các thương hiệu có tại shop: {blist}"
        else:
            return "Hiện chưa có thương hiệu nào trong hệ thống."

    # Trả lời về flash sale
    if any(kw in msg for kw in ['flash sale', 'giờ vàng', 'deal sốc', 'giảm giá mạnh']):
        # Giả sử Product có trường is_flash_sale
        flash_products = products.filter(is_flash_sale=True)
        if flash_products.exists():
            plist = '\n'.join([
                f"- {p.name}: Giá gốc {p.price:,}đ, giá flash sale {getattr(p, 'sale_price', p.price):,}đ" for p in flash_products
            ])
            return f"Các sản phẩm Flash Sale hôm nay:\n{plist}"
        else:
            return "Hiện chưa có sản phẩm Flash Sale nào."

    # Trả lời về đơn hàng
    if any(kw in msg for kw in ['đơn hàng', 'order', 'mua hàng', 'tình trạng đơn', 'kiểm tra đơn hàng']):
        return "Bạn có thể kiểm tra tình trạng đơn hàng bằng cách đăng nhập tài khoản hoặc liên hệ nhân viên tư vấn qua hotline, fanpage hoặc chat trực tiếp."
    msg = message.lower()
    # Luôn lấy dữ liệu sản phẩm mới nhất từ DB, không lưu cache
    products = Product.objects.filter(is_active=True)
    # Tìm theo xuất xứ/thương hiệu quốc gia
    countries = ['mỹ', 'hàn quốc', 'đức', 'pháp', 'nhật', 'trung', 'thái', 'anh', 'canada', 'italia', 'ý', 'tây ban nha']
    for country in countries:
        if country in msg:
            ps = products.filter(brand_origin__icontains=country)
            if ps.exists():
                plist = '\n'.join([f"- {p.name}: {p.description[:60]}... Giá: {p.price:,}đ | Xuất xứ: {p.brand_origin}" for p in ps[:5]])
                return f"Các sản phẩm xuất xứ từ {country.title()} của shop:\n{plist}"
            else:
                # Nếu không có sản phẩm khớp hoàn toàn, lấy các sản phẩm có brand_origin không rỗng
                ps = products.exclude(brand_origin__isnull=True).exclude(brand_origin__exact='')
                if ps.exists():
                    plist = '\n'.join([f"- {p.name}: {p.description[:60]}... Giá: {p.price:,}đ | Xuất xứ: {p.brand_origin}" for p in ps[:5]])
                    return f"Một số sản phẩm và xuất xứ của shop:\n{plist}"
    # Nếu hỏi về đặt hàng, trả lời tự động
    if any(kw in msg for kw in ['đặt hàng', 'mua', 'order', 'cách mua', 'cách đặt']):
        return "Bạn chỉ cần chọn sản phẩm, nhấn Mua ngay và điền thông tin để hoàn tất đơn hàng. Nếu cần hỗ trợ, hãy liên hệ shop!"
    # Nếu hỏi về khuyến mãi
    if any(kw in msg for kw in ['khuyến mãi', 'giảm giá', 'ưu đãi', 'sale', 'liệt kê khuyến mại', 'khuyến mại gì']):
        # Giả sử Product có trường 'promotion' hoặc 'discount' hoặc 'is_sale' hoặc 'sale_price'
        promo_products = products.filter(
            # Nếu có trường 'is_sale' hoặc 'sale_price', dùng filter phù hợp
            # is_sale=True hoặc sale_price__isnull=False hoặc promotion__isnull=False
            # Ở đây thử với sale_price
            sale_price__isnull=False
        )
        if promo_products.exists():
            plist = '\n'.join([
                f"- {p.name}:\n  Mô tả: {p.description[:60]}...\n  Giá gốc: {p.price:,}đ\n  Giá khuyến mãi: {getattr(p, 'sale_price', p.price):,}đ\n  Thương hiệu: {p.brand.name if p.brand else ''}\n  Loại da: {p.skin_type or ''}\n  Công dụng: {getattr(p, 'usage', '')}\n  Thành phần: {getattr(p, 'ingredients', '')}\n  Xuất xứ: {getattr(p, 'brand_origin', '')}"
                for p in promo_products
            ])
            return f"Các sản phẩm đang khuyến mãi tại shop:\n{plist}"
        else:
            return "Hiện tại shop chưa có sản phẩm nào đang khuyến mãi. Bạn có thể xem chi tiết tại trang Khuyến mãi hoặc hỏi nhân viên tư vấn nhé!"
    # Nếu hỏi về sản phẩm cụ thể
    for p in products:
        if p.name.lower() in msg:
            info = f"{p.name}: {p.description}\nGiá: {p.price:,}đ | Thương hiệu: {p.brand.name if p.brand else ''} | Loại da: {p.skin_type or 'Mọi loại da'}"
            return info
    # Phân loại sản phẩm rõ ràng theo nhóm và brand
    brands = Brand.objects.values_list('name', flat=True)
    product_types = [
        'son', 'kem chống nắng', 'sữa rửa mặt', 'serum', 'kem dưỡng', 'mặt nạ', 'tẩy trang', 'phấn', 'nước hoa hồng', 'toner', 'dưỡng ẩm',
        'kẻ mắt', 'eyeliner', 'mascara', 'kẻ mày', 'chì kẻ mắt', 'chì kẻ mày', 'bút kẻ mắt', 'bút kẻ mày'
    ]
    found_brand = None
    found_type = None
    for brand in brands:
        if brand.lower() in msg:
            found_brand = brand
            break
    for pt in product_types:
        if pt in msg:
            found_type = pt
            break
    # Nếu hỏi cả nhóm sản phẩm và brand
    if found_brand and found_type:
        ps = products.filter(brand__name__iexact=found_brand, name__icontains=found_type)
        if ps.exists():
            plist = '\n'.join([
                f"- {p.name}:\n  Mô tả: {p.description[:60]}...\n  Giá: {p.price:,}đ\n  Thương hiệu: {p.brand.name if p.brand else ''}\n  Loại da: {p.skin_type or ''}\n  Công dụng: {getattr(p, 'usage', '')}\n  Thành phần: {getattr(p, 'ingredients', '')}\n  Xuất xứ: {getattr(p, 'brand_origin', '')}"
                for p in ps
            ])
            return f"Các sản phẩm {found_type} của {found_brand} nổi bật:\n{plist}"
        else:
            return f"Hiện chưa có sản phẩm {found_type} của {found_brand} trong shop."
    # Nếu chỉ hỏi nhóm sản phẩm
    if found_type and not found_brand:
        ps = products.filter(name__icontains=found_type)
        if ps.exists():
            plist = '\n'.join([
                f"- {p.name}:\n  Mô tả: {p.description[:60]}...\n  Giá: {p.price:,}đ\n  Thương hiệu: {p.brand.name if p.brand else ''}\n  Loại da: {p.skin_type or ''}\n  Công dụng: {getattr(p, 'usage', '')}\n  Thành phần: {getattr(p, 'ingredients', '')}\n  Xuất xứ: {getattr(p, 'brand_origin', '')}"
                for p in ps
            ])
            return f"Các sản phẩm {found_type} của shop:\n{plist}"
        else:
            return f"Hiện chưa có sản phẩm {found_type} nào trong shop."
    # Nếu chỉ hỏi brand
    if found_brand and not found_type:
        ps = products.filter(brand__name__iexact=found_brand)
        if ps.exists():
            plist = '\n'.join([
                f"- {p.name}:\n  Mô tả: {p.description[:60]}...\n  Giá: {p.price:,}đ\n  Loại da: {p.skin_type or ''}\n  Công dụng: {getattr(p, 'usage', '')}\n  Thành phần: {getattr(p, 'ingredients', '')}\n  Xuất xứ: {getattr(p, 'brand_origin', '')}"
                for p in ps[:5]
            ])
            return f"Các sản phẩm của {found_brand} nổi bật:\n{plist}"
        else:
            return f"Hiện chưa có sản phẩm nào của {found_brand} trong shop."
    # Tìm theo loại da
    skin_types = ['dầu', 'da dầu', 'oil', 'oil skin', 'khô', 'da khô', 'hỗn hợp', 'nhạy cảm', 'mọi loại da']
    for st in skin_types:
        if st in msg:
            ps = products.filter(skin_type__icontains=st)
            if ps.exists():
                plist = '\n'.join([f"- {p.name}: {p.description[:60]}... Giá: {p.price:,}đ" for p in ps[:5]])
                return f"Các sản phẩm phù hợp cho da {st} của shop:\n{plist}"
            else:
                # Nếu không có sản phẩm khớp hoàn toàn, lấy các sản phẩm có skin_type không rỗng
                ps = products.exclude(skin_type__isnull=True).exclude(skin_type__exact='')
                if ps.exists():
                    plist = '\n'.join([f"- {p.name}: {p.description[:60]}... Giá: {p.price:,}đ | Loại da: {p.skin_type}" for p in ps[:5]])
                    return f"Một số sản phẩm và loại da phù hợp:\n{plist}"
    # Nếu hỏi về cách liên hệ
    if any(kw in msg for kw in ['liên hệ', 'tư vấn', 'gặp nhân viên', 'hỗ trợ']):
        return "Bạn có thể liên hệ shop qua hotline, fanpage hoặc chat trực tiếp với nhân viên tư vấn ở góc phải màn hình."

    # Nếu hỏi về nhóm sản phẩm (ví dụ: son, kem chống nắng, kẻ mắt...)
    product_types = [
        'son', 'kem chống nắng', 'sữa rửa mặt', 'serum', 'kem dưỡng', 'mặt nạ', 'tẩy trang', 'phấn', 'nước hoa hồng', 'toner', 'dưỡng ẩm',
        'kẻ mắt', 'eyeliner', 'mascara', 'kẻ mày', 'chì kẻ mắt', 'chì kẻ mày', 'bút kẻ mắt', 'bút kẻ mày'
    ]
    for pt in product_types:
        if pt in msg:
            ps = products.filter(name__icontains=pt)
            if ps.exists():
                plist = '\n'.join([f"- {p.name}: {p.description[:60]}... Giá: {p.price:,}đ" for p in ps])
                return f"Các sản phẩm {pt} của shop:\n{plist}"
    # Nếu không khớp nhóm nào, trả về danh sách tất cả sản phẩm
    if any(kw in msg for kw in ['sản phẩm', 'loại sản phẩm', 'danh sách sản phẩm', 'có những loại', 'có những sản phẩm']):
        ps = products.all()
        if ps.exists():
            plist = '\n'.join([f"- {p.name}: {p.description[:60]}... Giá: {p.price:,}đ" for p in ps])
            return f"Danh sách sản phẩm của shop:\n{plist}"
    return None

def call_openai_api(message):
    import requests
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return None
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    # Lấy dữ liệu sản phẩm
    product_info = find_product_info(message)
    # Luôn lấy dữ liệu sản phẩm mới nhất từ DB, không lưu cache
    all_products = Product.objects.filter(is_active=True)
    all_data = '\n'.join([
        f"- {p.name} | Giá: {p.price:,}đ | Thương hiệu: {p.brand.name if p.brand else ''} | Loại da: {p.skin_type or ''} | Công dụng: {getattr(p, 'usage', '')} | Thành phần: {getattr(p, 'ingredients', '')} | Xuất xứ: {getattr(p, 'brand_origin', '')} | Mô tả: {p.description[:60]}..." for p in all_products
    ])
    # Lấy top FAQ
    faqs = FAQ.objects.filter(is_active=True).order_by('-id')[:10]
    faq_data = '\n'.join([f"Q: {f.question}\nA: {f.answer}" for f in faqs])
    # Lấy lịch sử chat gần nhất
    recent_chats = ChatHistory.objects.order_by('-created_at')[:5]
    chat_history = '\n'.join([f"Khách: {c.message}\nBot: {c.bot_reply}" for c in recent_chats])
    # Prompt hệ thống ép trả lời tiếng Việt, học từ DB
    system_prompt = (
        "Bạn là trợ lý tư vấn mỹ phẩm cho shop Cosmetics, hãy trả lời ngắn gọn, thân thiện, ưu tiên sản phẩm của shop. Luôn trả lời bằng tiếng Việt. "
        "Hãy tư vấn dựa trên mọi thông tin sản phẩm, thương hiệu, công dụng, thành phần, loại da, xuất xứ... được cung cấp bên dưới. "
        "Bạn có thể học từ các câu hỏi thường gặp và lịch sử chat trước đó."
    )
    if product_info:
        system_prompt += f"\nDữ liệu sản phẩm liên quan: {product_info}"
    system_prompt += f"\n\nCác câu hỏi thường gặp:\n{faq_data}"
    system_prompt += f"\n\nLịch sử chat gần đây:\n{chat_history}"
    system_prompt += f"\n\nDữ liệu sản phẩm của shop:\n{all_data}"
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
    try:
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=10)
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content'].strip()
        else:
            print(f"OpenAI API error: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"OpenAI API exception: {e}")
    return "Xin lỗi, hệ thống AI đang bận hoặc gặp sự cố. Vui lòng thử lại sau hoặc liên hệ nhân viên tư vấn!"

@csrf_exempt
def chatbot_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Chỉ hỗ trợ POST'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message', '').strip()
        session_id = data.get('session_id', None)
        user_id = data.get('user_id', None)
    except Exception:
        return JsonResponse({'error': 'Dữ liệu không hợp lệ'}, status=400)
    if not message:
        return JsonResponse({'error': 'Vui lòng nhập câu hỏi'}, status=400)

    faqs = FAQ.objects.filter(is_active=True).order_by('-id')

    answer = (
        find_faq_by_tags(message, faqs)
        or find_faq_by_brand(message, faqs)
        or find_faq_by_question(message, faqs)
        or find_product_info(message)
    )
    if not answer:
        answer = call_openai_api(message)
    if not answer:
        answer = "Xin lỗi, tôi chưa có câu trả lời phù hợp. Vui lòng để lại thông tin, chúng tôi sẽ liên hệ lại!"

    # Lưu lịch sử chat
    user = None
    if user_id:
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
    ChatHistory.objects.create(
        user=user,
        session_id=session_id or '',
        message=message,
        bot_reply=answer,
        created_at=timezone.now()
    )
    return JsonResponse({'reply': answer})
