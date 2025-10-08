from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from products.models import Product

def remove_expired_flash_sale():
    now = timezone.now()
    updated = Product.objects.filter(is_promotion=True, sale_end__isnull=False, sale_end__lt=now).update(is_promotion=False)
    if updated:
        print(f"[Scheduler] Đã gỡ flash sale cho {updated} sản phẩm hết hạn lúc {now}.")
    else:
        print(f"[Scheduler] Không có sản phẩm flash sale nào hết hạn lúc {now}.")


def auto_set_flash_sale():
    now = timezone.now()
    import pytz
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now_vn = now.astimezone(vn_tz)
    flash_sale_duration = 60  # phút
    # Gỡ flash sale cho các sản phẩm đã hết hạn (phòng trường hợp job remove_expired_flash_sale chưa chạy kịp)
    Product.objects.filter(is_promotion=True, sale_end__isnull=False, sale_end__lt=now).update(is_promotion=False)
    # Chọn 5 sản phẩm tồn kho nhiều nhất, chưa flash sale, còn active
    products = Product.objects.filter(is_promotion=False, is_active=True, quantity_in_stock__gt=0).order_by('-quantity_in_stock')[:5]
    sale_end_time = now_vn + timezone.timedelta(minutes=flash_sale_duration)
    updated = 0
    for p in products:
        p.is_promotion = True
        p.sale_end = sale_end_time
        p.save(update_fields=['is_promotion', 'sale_end'])
        updated += 1
    if updated:
        print(f"[Scheduler] Đã tự động bật flash sale cho {updated} sản phẩm tồn kho nhiều nhất lúc {now_vn}.")
    else:
        print(f"[Scheduler] Không có sản phẩm nào đủ điều kiện để bật flash sale lúc {now_vn}.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    # Task gỡ flash sale cũ mỗi 60 phút
    scheduler.add_job(remove_expired_flash_sale, 'interval', minutes=60, id='remove_expired_flash_sale', replace_existing=True)
    # Task bật flash sale mỗi 60 phút (giữ nguyên)
    scheduler.add_job(auto_set_flash_sale, 'interval', minutes=60, id='auto_set_flash_sale', replace_existing=True)
    # Task bật flash sale mỗi 1 phút để sản phẩm mới thêm sẽ được flash sale gần như ngay lập tức
    scheduler.add_job(auto_set_flash_sale, 'interval', minutes=1, id='auto_set_flash_sale_fast', replace_existing=True)
    register_events(scheduler)
    scheduler.start()
