import random

def calculate_shipping_fee(address, weight_grams=500):
    """
    Giả lập tính phí ship từ GHTK/GHN.
    Trong thực tế, bạn sẽ gửi request tới API của họ.
    """
    # Phí cơ bản
    base_fee = 25000
    
    # Tính theo vùng miền (giả lập)
    if any(city in address.lower() for city in ['hồ chí minh', 'hcm', 'sài gòn']):
        location_multiplier = 1.0
    elif any(city in address.lower() for city in ['hà nội', 'hn']):
        location_multiplier = 1.5
    else:
        location_multiplier = 2.0
        
    # Tính theo khối lượng
    weight_fee = (weight_grams // 500) * 5000
    
    total_fee = (base_fee * location_multiplier) + weight_fee
    
    return {
        'fee': int(total_fee),
        'service_name': 'Giao Hàng Tiết Kiệm (GHTK)',
        'estimated_delivery': '2-4 ngày'
    }

def get_tracking_status(tracking_number):
    """
    Giả lập lấy trạng thái vận đơn.
    """
    statuses = [
        'Đã tiếp nhận', 
        'Đang lấy hàng', 
        'Đã nhập kho', 
        'Đang luân chuyển', 
        'Đang giao hàng', 
        'Giao hàng thành công'
    ]
    import hashlib
    # Dựa vào số vận đơn để lấy trạng thái cố định cho số đó
    idx = int(hashlib.md5(tracking_number.encode()).hexdigest(), 16) % len(statuses)
    
    return {
        'status': statuses[idx],
        'tracking_number': tracking_number,
        'carrier': 'GHTK'
    }
