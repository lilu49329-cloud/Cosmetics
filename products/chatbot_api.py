
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
    msg = message.lower()
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
    
    # Luôn lấy dữ liệu sản phẩm mới nhất từ DB, không lưu cache
    products = Product.objects.filter(is_active=True)
    # Tìm theo xuất xứ/thương hiệu quốc gia
    countries = ['mỹ', 'hàn quốc', 'đức', 'pháp', 'nhật', 'trung', 'thái', 'anh', 'canada', 'italia', 'ý', 'tây ban nha']
    for country in countries:
        if country in msg:
            ps = products.filter(brand_origin__icontains=country)
            if ps.exists():
                p = ps.first()
                return f"Dạ, shop có sản phẩm {p.name} (Hãng {p.brand.name if p.brand else 'Đang cập nhật'}). Không biết tình trạng da hiện tại của bạn như thế nào để mình tư vấn kỹ hơn ạ?"
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
            p = promo_products.first()
            return f"Hiện shop đang có deal hời cho {p.name} (Hãng {p.brand.name if p.brand else ''}). Bạn cần tư vấn cho tình trạng da nào ạ?"
        else:
            return "Hiện tại shop chưa có sản phẩm nào đang khuyến mãi. Bạn có thể xem chi tiết tại trang Khuyến mãi hoặc hỏi nhân viên tư vấn nhé!"
    # Nếu hỏi về sản phẩm cụ thể
    for p in products:
        if p.name.lower() in msg:
            if any(kw in msg for kw in ['tác dụng', 'công dụng', 'dùng làm gì', 'có tốt không', 'hiệu quả']):
                return f"{p.name}: {p.description}\nGiá: {p.price:,}đ | Loại da: {p.skin_type or 'Mọi loại da'}"
            return f"Dạ, đó là {p.name} của hãng {p.brand.name if p.brand else ''}. Bạn đang gặp vấn đề gì về da để mình tư vấn xem sản phẩm này có phù hợp không nhé?"
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
            p = ps.first()
            return f"Dạ, shop có {p.name} của hãng {found_brand}. Bạn đang gặp tình trạng da như thế nào để mình xem sản phẩm này có giúp được gì không ạ?"
        else:
            return f"Hiện chưa có sản phẩm {found_type} của {found_brand} trong shop."
    # Nếu chỉ hỏi nhóm sản phẩm
    if found_type and not found_brand:
        ps = products.filter(name__icontains=found_type)
        if ps.exists():
            p = ps.first()
            return f"Dạ, shop có {p.name} (Hãng {p.brand.name if p.brand else ''}). Bạn cần tư vấn cho tình trạng da cụ thể nào không ạ?"
        else:
            return f"Hiện chưa có sản phẩm {found_type} nào trong shop."
    # Nếu chỉ hỏi brand
    if found_brand and not found_type:
        ps = products.filter(brand__name__iexact=found_brand)
        if ps.exists():
            p = ps.first()
            return f"Dạ, hãng {found_brand} có sản phẩm {p.name} rất nổi tiếng. Bạn đang gặp vấn đề gì về da để mình tư vấn kỹ hơn cho bạn nhé?"
        else:
            return f"Hiện chưa có sản phẩm nào của {found_brand} trong shop."
    # Tìm theo loại da
    skin_types = ['dầu', 'da dầu', 'oil', 'oil skin', 'khô', 'da khô', 'hỗn hợp', 'nhạy cảm', 'mọi loại da']
    for st in skin_types:
        if st in msg:
            ps = products.filter(skin_type__icontains=st)
            if ps.exists():
                p = ps.first()
                return f"Cho da {st}, tôi gợi ý sản phẩm: {p.name}. Giá: {p.price:,}đ. Sản phẩm này rất được ưa chuộng!"
            else:
                return f"Hiện chưa có sản phẩm cụ thể cho da {st}, bạn có thể xem các loại dùng cho mọi loại da nhé."
    # Bỏ phần chặn từ khóa 'tư vấn' để AI có thể xử lý linh hoạt hơn
    pass

    # Xóa bỏ các loop lặp lại
    pass
    # Nếu không khớp nhóm nào, trả về danh sách tất cả sản phẩm
    if any(kw in msg for kw in ['sản phẩm', 'loại sản phẩm', 'danh sách sản phẩm', 'có những loại', 'có những sản phẩm']):
        return "Shop có rất nhiều sản phẩm đa dạng từ chăm sóc da đến trang điểm. Bạn đang quan tâm đến nhóm sản phẩm nào (ví dụ: son, tẩy trang, kem dưỡng...)?"
    return None

def call_openai_api(message, session_id=None):
    import requests
    from django.conf import settings
    api_key = getattr(settings, 'OPENAI_API_KEY', os.environ.get('OPENAI_API_KEY'))
    if not api_key:
        return "Xin lỗi, hệ thống AI (OpenAI) chưa được cấu hình khóa API. Vui lòng liên hệ quản trị viên."
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
    # Lấy lịch sử chat của phiên hiện tại (session_id) để tránh lặp
    recent_chats = ChatHistory.objects.filter(session_id=session_id).order_by('-created_at')[:5] if session_id else ChatHistory.objects.order_by('-created_at')[:5]
    chat_history = '\n'.join([f"Khách: {c.message}\nBot: {c.bot_reply}" for c in reversed(recent_chats)])
    system_prompt = (
        "Bạn là chuyên gia tư vấn mỹ phẩm cao cấp. Quy trình tư vấn của bạn PHẢI tuân thủ các bước sau: "
        "1. Khi khách hỏi về sản phẩm/loại sản phẩm, CHỈ trả lời Tên sản phẩm và Tên hãng. "
        "2. Sau đó, hãy hỏi khách về Tình trạng da hoặc Vấn đề họ đang gặp phải. "
        "3. CHỈ giải thích công dụng, thành phần khi khách hỏi chi tiết (ví dụ: 'nó có tác dụng gì?', 'dùng thế nào?'). "
        "TRÁNH nói quá nhiều ngay từ đầu. Luôn ngắn gọn, thân thiện và chuyên nghiệp bằng tiếng Việt."
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

    # Nhận diện các yêu cầu đổi sản phẩm hoặc tư vấn thêm
    is_asking_other = any(kw in message.lower() for kw in ['khác', 'đổi', 'thêm', 'nữa', 'thay'])
    
    # Nếu yêu cầu đổi loại khác, bỏ qua logic tìm kiếm cứng và chuyển cho AI
    if is_asking_other:
        answer = call_openai_api(message, session_id)
    else:
        answer = (
            find_faq_by_tags(message, faqs)
            or find_faq_by_brand(message, faqs)
            or find_faq_by_question(message, faqs)
            or find_product_info(message)
        )
        if not answer:
            answer = call_openai_api(message, session_id)
            
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
