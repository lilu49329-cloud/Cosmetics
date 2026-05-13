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

def create_detailed_news():
    news_items = [
        {
            "title": "Xu hướng trang điểm mùa hè 2026: Rạng rỡ và Tự nhiên",
            "content": """Mùa hè 2026 đang đến gần, mang theo những làn sóng mới trong thế giới làm đẹp. Năm nay, xu hướng 'Clean Girl' tiếp tục tiến hóa thành một phong cách rạng rỡ và có chiều sâu hơn.

Điểm nhấn lớn nhất chính là làn da 'Glowy' nhưng không bóng dầu. Các chuyên gia trang điểm hàng đầu khuyên bạn nên sử dụng các loại kem lót bắt sáng kết hợp với kem nền mỏng nhẹ để tạo hiệu ứng da ngậm nước tự nhiên.

Về màu sắc, tông màu cam đào (Peach Fuzz) và hồng san hô đang chiếm lĩnh các sàn diễn thời trang. Đôi môi mọng nước với son bóng và gò má ửng hồng tự nhiên là những yếu tố không thể thiếu. Ngoài ra, xu hướng vẽ tàn nhang giả cũng đang quay trở lại, mang đến vẻ ngoài tinh nghịch và trẻ trung cho những buổi dã ngoại ngoài trời.

Đừng quên bảo vệ làn da của bạn bằng kem chống nắng có độ phổ rộng trước khi bắt đầu quy trình trang điểm. Hãy cùng Cosmetics cập nhật những sản phẩm mới nhất để luôn tỏa sáng trong mùa hè này!""",
            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800"
        },
        {
            "title": "Bí quyết chăm sóc da khô vào mùa đông: Quy trình 5 bước chuyên sâu",
            "content": """Thời tiết hanh khô của mùa đông là 'kẻ thù' số một của làn da, đặc biệt là da khô và da nhạy cảm. Để giữ cho làn da luôn mềm mịn và căng tràn sức sống, bạn cần một quy trình chăm sóc đặc biệt.

Bước 1: Làm sạch nhẹ nhàng. Hãy ưu tiên các loại sữa rửa mặt dạng gel hoặc sữa có độ pH cân bằng, tránh các loại có chất tẩy rửa mạnh làm mất đi lớp dầu tự nhiên trên da.

Bước 2: Cấp ẩm tức thì với Toner. Ngay sau khi rửa mặt, hãy dùng toner không cồn để làm dịu và chuẩn bị cho các bước dưỡng tiếp theo.

Bước 3: Serum phục hồi. Sử dụng các loại serum chứa Hyaluronic Acid hoặc Vitamin B5 để cấp nước sâu vào các tầng biểu bì.

Bước 4: Khóa ẩm với kem dưỡng chuyên sâu. Một loại kem dưỡng đặc, giàu Ceramide sẽ giúp tạo lớp màng bảo vệ, ngăn ngừa tình trạng mất nước xuyên biểu bì.

Bước 5: Đừng bỏ qua kem chống nắng. Dù là mùa đông, tia UV vẫn tồn tại và có thể gây tổn thương da. Hãy luôn sử dụng kem chống nắng trước khi ra ngoài.

Hãy nhớ uống đủ 2 lít nước mỗi ngày và bổ sung các loại thực phẩm giàu Omega-3 để nuôi dưỡng làn da từ bên trong nhé!""",
            "image_url": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=800"
        },
        {
            "title": "Đại tiệc khai trương: Cosmetics chính thức có mặt tại Hà Đông",
            "content": """Sau bao ngày chờ đợi, Cosmetics vô cùng hào hứng thông báo về việc khai trương chi nhánh thứ 3 tại khu vực Hà Đông. Đây là bước tiến quan trọng trong hành trình mang cái đẹp đến gần hơn với mọi khách hàng.

Tọa lạc tại vị trí đắc địa số 637 QL6, Phú La, Hà Đông, cửa hàng mới được thiết kế với không gian hiện đại, sang trọng cùng khu vực trải nghiệm sản phẩm (Tester) hoàn toàn miễn phí. Tại đây, bạn có thể tìm thấy hơn 1000 mã sản phẩm từ các thương hiệu nổi tiếng như Maybelline, La Roche-Posay, Bioderma, E.L.F và nhiều hơn nữa.

Nhân dịp khai trương, chúng tôi mang đến chương trình ưu đãi 'Cực Khủng':
- Giảm giá lên đến 50% cho toàn bộ sản phẩm trong 3 ngày đầu tiên.
- Tặng 100 phần quà trị giá 500k cho 100 khách hàng đầu tiên mỗi ngày.
- Soi da và tư vấn chăm sóc da hoàn toàn miễn phí cùng chuyên gia.

Hãy rủ ngay hội chị em bạn dì đến check-in và nhận quà tại Cosmetics Hà Đông vào cuối tuần này nhé. Chúng tôi rất mong được đón tiếp bạn!""",
            "image_url": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800"
        }
    ]

    # Clear old news
    News.objects.all().delete()
    
    for i, item in enumerate(news_items, 1):
        obj = News.objects.create(
            id=i,
            title=item['title'],
            content=item['content']
        )
        
        # Always try to refresh image for quality
        try:
            resp = requests.get(item['image_url'], timeout=10)
            if resp.status_code == 200:
                # Delete old image if exists to keep it clean
                if obj.image:
                    try:
                        os.remove(obj.image.path)
                    except:
                        pass
                obj.image.save(f"news_full_{obj.id}.jpg", ContentFile(resp.content), save=True)
        except:
            pass

if __name__ == '__main__':
    create_detailed_news()
