from .models import Product
from django.db.models import Q

def get_smart_recommendations(product, limit=4):
    """
    Gợi ý sản phẩm thông minh dựa trên:
    1. Cùng loại da (skin_type)
    2. Cùng công dụng (usage)
    3. Cùng thương hiệu (brand)
    """
    recommendations = Product.objects.filter(is_active=True).exclude(id=product.id)
    
    # Ưu tiên sản phẩm cùng loại da và công dụng
    filters = Q()
    if product.skin_type:
        filters |= Q(skin_type__icontains=product.skin_type)
    if product.usage:
        filters |= Q(usage__icontains=product.usage)
    
    if filters:
        recommendations = recommendations.filter(filters)
    
    # Nếu ít quá thì lấy thêm cùng category
    if recommendations.count() < limit:
        extra = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id).exclude(id__in=recommendations.values_list('id', flat=True))
        recommendations = list(recommendations) + list(extra[:limit - len(recommendations)])
    else:
        recommendations = recommendations[:limit]
        
    return recommendations

def analyze_skin_type(image_file):
    """
    Phân tích da thực tế bằng OpenAI Vision API.
    """
    import base64
    import requests
    from django.conf import settings
    import os

    api_key = getattr(settings, 'OPENAI_API_KEY', os.environ.get('OPENAI_API_KEY'))
    if not api_key or 'your-openai' in api_key:
        # Fallback nếu không có API key
        return {
            'status': 'demo',
            'skin_type': 'Da hỗn hợp (Demo)',
            'concerns': ['Cần cấu hình API Key'],
            'confidence': 1.0
        }

    try:
        # Đọc và mã hóa ảnh sang base64
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Phân tích tình trạng da từ bức ảnh này. Trả về kết quả dưới dạng JSON với các trường: 'skin_type' (Da dầu, Da khô, Da hỗn hợp, Da nhạy cảm), 'concerns' (danh sách tối đa 3 vấn đề như Mụn, Nám, Lỗ chân lông to, Nếp nhăn), 'confidence' (số từ 0-100). Chỉ trả về JSON."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=15)
        res_json = response.json()
        content = res_json['choices'][0]['message']['content']
        
        # Làm sạch chuỗi JSON nếu AI trả về kèm markdown
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            import json
            result = json.loads(json_match.group())
            return {
                'status': 'success',
                'skin_type': result.get('skin_type', 'Da hỗn hợp'),
                'concerns': result.get('concerns', ['Lỗ chân lông to']),
                'confidence': result.get('confidence', 80.0)
            }
    except Exception as e:
        print(f"AI Analysis Error: {e}")

    return {
        'status': 'error',
        'skin_type': 'Chưa xác định',
        'concerns': ['Cần thử lại'],
        'confidence': 0
    }
