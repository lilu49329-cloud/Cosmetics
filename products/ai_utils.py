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

def analyze_skin_type(image_path):
    """
    Giả lập phân tích da từ hình ảnh.
    Trong thực tế, đây sẽ là nơi gọi model AI (TensorFlow/PyTorch) hoặc API bên thứ 3.
    """
    # Đây là logic giả lập
    # Chúng ta có thể trả về các thuộc tính như: 'da_dau', 'da_kho', 'mun', 'nam'
    import random
    results = {
        'status': 'success',
        'skin_type': random.choice(['Da dầu', 'Da khô', 'Da hỗn hợp', 'Da nhạy cảm']),
        'concerns': random.sample(['Mụn', 'Lỗ chân lông to', 'Sắc tố da', 'Nếp nhăn'], k=2),
        'confidence': 0.85
    }
    return results
