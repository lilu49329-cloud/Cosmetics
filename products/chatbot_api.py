
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
    if any(kw in msg for kw in ['khuyến mãi', 'giảm giá', 'ưu đãi', 'sale']):
        return "Shop luôn có nhiều khuyến mãi hấp dẫn, bạn xem chi tiết tại trang Khuyến mãi hoặc hỏi nhân viên tư vấn nhé!"
    # Nếu hỏi về sản phẩm cụ thể
    for p in products:
        if p.name.lower() in msg:
            info = f"{p.name}: {p.description}\nGiá: {p.price:,}đ | Thương hiệu: {p.brand.name if p.brand else ''} | Loại da: {p.skin_type or 'Mọi loại da'}"
            return info
    # Tìm theo brand
    brands = Brand.objects.values_list('name', flat=True)
    for brand in brands:
        if brand.lower() in msg:
            ps = products.filter(brand__name__iexact=brand)
            if ps.exists():
                plist = ', '.join([p.name for p in ps[:5]])
                return f"Các sản phẩm của {brand}: {plist}"
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

    # Nếu hỏi về nhóm sản phẩm (ví dụ: son, kem chống nắng...)
    product_types = ['son', 'kem chống nắng', 'sữa rửa mặt', 'serum', 'kem dưỡng', 'mặt nạ', 'tẩy trang', 'phấn', 'nước hoa hồng', 'toner', 'dưỡng ẩm']
    for pt in product_types:
        if pt in msg:
            ps = products.filter(name__icontains=pt)
            if ps.exists():
                # Trả về danh sách sản phẩm dạng mô tả để truyền vào AI
                plist = '\n'.join([f"- {p.name}: {p.description[:60]}... Giá: {p.price:,}đ" for p in ps[:5]])
                return f"Các sản phẩm {pt} nổi bật của shop:\n{plist}"
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
    # Đưa thông tin sản phẩm vào prompt nếu có
    product_info = find_product_info(message)
    # Lấy toàn bộ dữ liệu sản phẩm nếu không có câu trả lời cụ thể
    all_products = Product.objects.filter(is_active=True)
    all_data = '\n'.join([
        f"- {p.name} | Giá: {p.price:,}đ | Thương hiệu: {p.brand.name if p.brand else ''} | Loại da: {p.skin_type or ''} | Công dụng: {getattr(p, 'usage', '')} | Thành phần: {getattr(p, 'ingredients', '')} | Xuất xứ: {getattr(p, 'brand_origin', '')} | Mô tả: {p.description[:60]}..." for p in all_products[:15]
    ])
    system_prompt = "Bạn là trợ lý tư vấn mỹ phẩm cho shop Cosmetics, hãy trả lời ngắn gọn, thân thiện, ưu tiên sản phẩm của shop. Hãy tư vấn dựa trên mọi thông tin sản phẩm, thương hiệu, công dụng, thành phần, loại da, xuất xứ... được cung cấp bên dưới."
    # Luôn truyền dữ liệu sản phẩm vào prompt, kể cả khi có product_info
    if product_info:
        system_prompt += f"\nDữ liệu sản phẩm liên quan: {product_info}"
    system_prompt += f"\nDữ liệu sản phẩm của shop:\n{all_data}"
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "max_tokens": 200
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
