import os
import django
import sys
from django.utils import timezone
import requests
from django.core.files.base import ContentFile

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import News

def create_dummy_news():
    news_items = [
        {
            "title": "Xu hướng trang điểm mùa hè 2026",
            "content": "Khám phá những phong cách trang điểm mới nhất cho mùa hè năm nay với các tông màu rực rỡ và tươi mới. Làn da căng bóng và đôi môi màu cam đào đang lên ngôi...",
            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600"
        },
        {
            "title": "Bí quyết chăm sóc da khô vào mùa đông",
            "content": "Dưỡng ẩm là chìa khóa quan trọng nhất. Hãy cùng tìm hiểu quy trình 5 bước để giữ cho làn da luôn mềm mại và không bị bong tróc trong thời tiết hanh khô...",
            "image_url": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=600"
        },
        {
            "title": "Khai trương chi nhánh mới tại Hà Đông",
            "content": "Chào mừng chi nhánh thứ 3 của chúng tôi chính thức đi vào hoạt động tại 637 QL6, Phú La, Hà Đông. Hàng ngàn phần quà hấp dẫn đang chờ đón quý khách...",
            "image_url": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600"
        }
    ]

    for item in news_items:
        obj, created = News.objects.update_or_create(
            title=item['title'],
            defaults={
                'content': item['content'],
            }
        )
        
        if not obj.image:
            try:
                resp = requests.get(item['image_url'], timeout=10)
                if resp.status_code == 200:
                    obj.image.save(f"news_{obj.id}.jpg", ContentFile(resp.content), save=True)
            except:
                pass

if __name__ == '__main__':
    create_dummy_news()
