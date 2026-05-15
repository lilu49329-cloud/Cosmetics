import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import News

def sync_news():
    print("--- Dang dong bo Tin tuc ---")
    n_files = [f for f in os.listdir('media/news') if os.path.isfile(os.path.join('media/news', f))]
    
    # 1. Cap nhat tin hien co
    existing_news = News.objects.all()
    for n in existing_news:
        if n_files:
            n.image = f"news/{random.choice(n_files)}"
            n.save()
            # print(f"OK: Da cap nhat anh cho tin: {n.title}")

    # 2. Them tin moi neu it qua
    if existing_news.count() < 3:
        new_titles = [
            "Bí quyết chăm sóc da mùa hanh khô",
            "Top 5 thỏi son không thể thiếu trong túi xách",
            "Xu hướng trang điểm tự nhiên 2025"
        ]
        for title in new_titles:
            content = "Đây là nội dung chia sẻ về bí quyết làm đẹp và các xu hướng mỹ phẩm mới nhất giúp bạn luôn tự tin và tỏa sáng mỗi ngày..."
            News.objects.create(
                title=title,
                content=content,
                image=f"news/{random.choice(n_files)}" if n_files else None
            )
            # print(f"OK: Da tao tin moi: {title}")

    print("--- Hoan tat dong bo Tin tuc ---")

if __name__ == "__main__":
    sync_news()
