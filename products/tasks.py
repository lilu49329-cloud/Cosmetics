from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from products.models import Product

def remove_expired_flash_sale():
    now = timezone.now()
    updated = Product.objects.filter(is_promotion=True, sale_end__isnull=False, sale_end__lt=now).update(is_promotion=False)
    if updated:
        print(f"[Scheduler] Flash sale removed for {updated} expired products at {now}.")
    else:
        print(f"[Scheduler] No expired flash sale products found at {now}.")


def auto_set_flash_sale():
    now = timezone.now()
    import pytz
    import random
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now_vn = now.astimezone(vn_tz)
    
    # Cấu hình vòng lặp
    flash_sale_duration = 10  # Mỗi đợt kéo dài 10 phút
    max_flash_products = 5    # Luôn duy trì 5 sản phẩm trong Flash Sale
    
    # 1. Gỡ các sản phẩm đã hết hạn
    expired = Product.objects.filter(is_promotion=True, sale_end__isnull=False, sale_end__lt=now)
    expired_count = expired.count()
    expired.update(is_promotion=False)
    
    if expired_count:
        print(f"[Scheduler] Đã gỡ {expired_count} sản phẩm hết hạn.")

    # 2. Kiểm tra số lượng sản phẩm đang Flash Sale hiện tại
    current_count = Product.objects.filter(is_promotion=True, is_active=True).count()
    needed_count = max_flash_products - current_count
    
    if needed_count > 0:
        # Chọn các sản phẩm: 
        # - Đang không trong promotion
        # - Còn active và còn hàng
        # - Sắp xếp theo updated_at tăng dần (những con "lâu rồi chưa được lên sóng")
        potential_pool = Product.objects.filter(
            is_promotion=False, 
            is_active=True, 
            quantity_in_stock__gt=0
        ).order_by('updated_at')[:15] # Lấy top 15 ứng viên "cũ" nhất
        
        candidates = list(potential_pool)
        if candidates:
            # Lấy ngẫu nhiên từ pool để tăng tính luân phiên
            selected_products = random.sample(candidates, min(len(candidates), needed_count))
            
            sale_end_time = now + timezone.timedelta(minutes=flash_sale_duration)
            for p in selected_products:
                p.is_promotion = True
                p.sale_end = sale_end_time
                # Save sẽ tự động cập nhật updated_at, đẩy sản phẩm này xuống cuối hàng đợi cho lần sau
                p.save(update_fields=['is_promotion', 'sale_end', 'updated_at'])
            
            print(f"[Scheduler] Đã luân phiên thêm {len(selected_products)} sản phẩm mới vào Flash Sale. Tổng cộng hiện có {Product.objects.filter(is_promotion=True).count()} sản phẩm.")
        else:
            print("[Scheduler] Không còn sản phẩm nào đủ điều kiện để luân phiên.")
    else:
        print(f"[Scheduler] Flash Sale đang đủ {current_count} sản phẩm, không cần thêm.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    
    # Chạy kiểm tra và luân phiên mỗi 1 phút
    scheduler.add_job(auto_set_flash_sale, 'interval', minutes=1, id='auto_set_flash_sale_loop', replace_existing=True)
    
    register_events(scheduler)
    scheduler.start()
