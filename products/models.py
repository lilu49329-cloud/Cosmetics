from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# --- Models ---
# Slider model
class Slider(models.Model):
    title = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='slider/', blank=False)
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0, help_text='Thứ tự hiển thị, có thể kéo thả trong admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Slider/Banner'
        verbose_name_plural = 'Quản lý Slider/Banner'
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.title or f"Slider #{self.id}"
# --- Chatbot Models ---
class FAQ(models.Model):
    question = models.CharField("Câu hỏi thường gặp", max_length=255, unique=True)
    answer = models.TextField("Câu trả lời")
    tags = models.CharField("Từ khóa liên quan", max_length=255, blank=True, help_text="Phân tách bởi dấu phẩy, ví dụ: son, môi, đỏ")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Câu hỏi thường gặp (FAQ)"
        verbose_name_plural = "Câu hỏi thường gặp (FAQ)"

    def __str__(self):
        return self.question

class ChatHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=64, blank=True, db_index=True)
    message = models.TextField("Tin nhắn người dùng")
    bot_reply = models.TextField("Phản hồi của bot")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lịch sử chat chatbot"
        verbose_name_plural = "Lịch sử chat chatbot"
        ordering = ["-created_at"]
from django.db import models
# Model thương hiệu
class Brand(models.Model):
    name = models.TextField("Tên thương hiệu", unique=True)
    logo = models.ImageField("Logo thương hiệu", upload_to="brands/", blank=True, null=True)

    class Meta:
        verbose_name = "Thương hiệu"
        verbose_name_plural = "Quản lý Thương hiệu"

    def __str__(self):
        return self.name
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Hồ sơ người dùng mở rộng
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    points = models.IntegerField(default=0)
    
    @property
    def membership_tier(self):
        if self.points >= 5000:
            return "Kim cương (Diamond)"
        elif self.points >= 2000:
            return "Vàng (Gold)"
        elif self.points >= 1000:
            return "Bạc (Silver)"
        else:
            return "Đồng (Bronze)"
            
    @property
    def discount_rate(self):
        # Tỷ lệ giảm giá dựa trên hạng thành viên
        if self.points >= 5000: return 0.15 # 15%
        if self.points >= 2000: return 0.10 # 10%
        if self.points >= 1000: return 0.05 # 5%
        return 0

    def __str__(self):
        return self.user.username

# Tự động tạo UserProfile khi tạo User
@receiver(post_save, sender=User)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Thông báo cho người dùng
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Thông báo"
        verbose_name_plural = "Quản lý Thông báo"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user}: {self.message}"

class HotDealBanner(models.Model):
    """Banner ảnh cho Hot Deals"""
    title = models.CharField("Tiêu đề banner", max_length=200, blank=True)
    image = models.ImageField("Ảnh banner Hot Deals", upload_to="hotdeals/", blank=False, null=False)
    link = models.URLField("Liên kết khi click", blank=True)
    is_active = models.BooleanField("Hiển thị", default=True)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    updated_at = models.DateTimeField("Ngày cập nhật", auto_now=True)

    class Meta:
        verbose_name = "Hot Deal Banner"
        verbose_name_plural = "Hot Deal Banners"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"Banner #{self.id}"

from django.db import models

class Promotion(models.Model):
    """Khuyến mãi cho sản phẩm"""
    name = models.TextField("Tên khuyến mãi")
    description = models.TextField("Mô tả", blank=True)
    discount_percent = models.PositiveIntegerField("Phần trăm giảm giá", default=0)
    start_date = models.DateTimeField("Ngày bắt đầu")
    end_date = models.DateTimeField("Ngày kết thúc")
    products = models.ManyToManyField('Product', related_name='promotions', blank=True)

    class Meta:
        verbose_name = "Khuyến mãi"
        verbose_name_plural = "Quản lý Khuyến mãi"

    def __str__(self):
        return self.name

class Category(models.Model):
    """Danh mục sản phẩm mỹ phẩm"""
    name = models.TextField("Tên danh mục", unique=True)
    description = models.TextField("Mô tả", blank=True)

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Quản lý Danh mục"

    def __str__(self):
        return self.name

class Product(models.Model):
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Quản lý Sản phẩm"

    brand_origin = models.TextField("Xuất xứ thương hiệu", blank=True, null=True)
    texture = models.TextField("Kết cấu", blank=True, null=True)
    skin_type = models.TextField("Loại da", blank=True, null=True)
    """Sản phẩm mỹ phẩm"""
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.TextField("Tên sản phẩm")
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Thương hiệu")
    description = models.TextField("Mô tả", blank=True)
    ingredients = models.TextField("Thành phần", blank=True)
    usage = models.TextField("Công dụng", blank=True)
    how_to_use = models.TextField("Cách dùng", blank=True)
    quantity_in_stock = models.PositiveIntegerField("Tồn kho", default=0)
    created_at = models.DateTimeField("Ngày thêm", auto_now_add=True)
    updated_at = models.DateTimeField("Ngày cập nhật", auto_now=True)
    is_active = models.BooleanField("Còn kinh doanh", default=True)
    is_hot = models.BooleanField("Sản phẩm hot", default=False)
    image = models.ImageField("Ảnh sản phẩm (chính)", upload_to="products/", blank=True, null=True)
    is_promotion = models.BooleanField("Khuyến mãi", default=False)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    sale_end = models.DateTimeField("Ngày kết thúc Flash Sale", blank=True, null=True)
    has_gift = models.BooleanField("Có quà tặng", default=False)

    # ...existing code...
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Ảnh phụ", upload_to="products/extra/", blank=False, null=False)
    alt_text = models.CharField("Mô tả ảnh", max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ảnh sản phẩm"
        verbose_name_plural = "Quản lý Ảnh sản phẩm"


class Store(models.Model):
    """Cửa hàng hệ thống"""
    name = models.TextField("Tên cửa hàng")
    address = models.CharField("Địa chỉ", max_length=255)
    phone = models.CharField("Điện thoại", max_length=20, blank=True)

    class Meta:
        verbose_name = "Cửa hàng"
        verbose_name_plural = "Quản lý Cửa hàng"

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Đánh giá sản phẩm"
        verbose_name_plural = "Đánh giá sản phẩm"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} đánh giá {self.product} ({self.rating} sao)"

class Customer(models.Model):
    """Thông tin khách hàng"""
    full_name = models.TextField("Họ tên")
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Điện thoại", max_length=20, blank=True)
    address = models.CharField("Địa chỉ", max_length=255, blank=True)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    updated_at = models.DateTimeField("Ngày cập nhật", auto_now=True)

    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Quản lý Khách hàng"

    def __str__(self):
        return self.full_name

class Order(models.Model):
    """Đơn hàng"""
    PAYMENT_METHODS = [
        ("cod", "Thanh toán khi nhận hàng (COD)"),
        ("bank", "Chuyển khoản ngân hàng"),
        ("momo", "Ví MoMo"),
        ("vnpay", "VNPay"),
        ("zalopay", "ZaloPay"),
        ("credit", "Thẻ tín dụng/Ghi nợ")
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name="orders")
    order_date = models.DateTimeField("Ngày đặt hàng", auto_now_add=True)
    shipped_date = models.DateTimeField("Ngày giao hàng", null=True, blank=True)
    status = models.CharField(
        "Trạng thái",
        max_length=20,
        choices=[
            ("pending", "Chờ xác nhận"),
            ("confirmed", "Đã xác nhận"),
            ("shipped", "Đã gửi hàng"),
            ("completed", "Hoàn thành"),
            ("canceled", "Đã hủy")
        ],
        default="pending"
    )
    payment_method = models.CharField("Hình thức thanh toán", max_length=20, choices=PAYMENT_METHODS, default="cod")
    is_paid = models.BooleanField("Đã thanh toán", default=False)
    transaction_id = models.CharField("Mã giao dịch", max_length=100, blank=True, null=True)
    shipping_address = models.CharField("Địa chỉ giao hàng", max_length=255, default="", blank=True)
    total_amount = models.DecimalField("Tổng tiền", max_digits=14, decimal_places=2, default=0)
    shipping_fee = models.DecimalField("Phí vận chuyển", max_digits=10, decimal_places=2, default=0)
    tracking_number = models.CharField("Mã vận đơn", max_length=50, blank=True, null=True)
    note = models.TextField("Ghi chú", blank=True)

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Quản lý Đơn hàng"
        ordering = ["-order_date"]

    def __str__(self):
        if self.customer and hasattr(self.customer, 'full_name'):
            return f"Đơn hàng #{self.id} - {self.customer.full_name}"
        return f"Đơn hàng #{self.id}"

    def calculate_total(self):
        """Tính tổng tiền đơn hàng từ các items"""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()
        return total

class OrderItem(models.Model):
    """Chi tiết đơn hàng"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="order_items")
    product_name = models.TextField("Tên sản phẩm")  # Lưu tên sản phẩm tại thời điểm đặt hàng
    price = models.DecimalField("Đơn giá", max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField("Số lượng", default=1)

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return f"{self.product_name} ({self.quantity})"

    @property
    def subtotal(self):
        """Tính thành tiền"""
        return self.price * self.quantity

class News(models.Model):
    title = models.CharField("Tiêu đề", max_length=255)
    content = models.TextField("Nội dung")
    image = models.ImageField("Ảnh minh họa", upload_to="news/", blank=True, null=True)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)

    class Meta:
        verbose_name = "Tin tức"
        verbose_name_plural = "Tin tức"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
