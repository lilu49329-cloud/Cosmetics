
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Customer, Order, ProductImage, HotDealBanner, News, Brand, Store, FAQ, ChatHistory

# Đăng ký FAQ và ChatHistory vào admin
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active", "tags")
    search_fields = ("question", "answer", "tags")
    list_filter = ("is_active",)

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "session_id", "message", "created_at")
    search_fields = ("user__username", "session_id", "message", "bot_reply")
    list_filter = ("created_at",)

# Đăng ký Store để quản lý cửa hàng trong admin
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone")
    search_fields = ("name", "address", "phone")


# Inline cho nhiều ảnh phụ
class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1
	fields = ("image", "alt_text", "uploaded_at", "image_preview")
	readonly_fields = ("uploaded_at", "image_preview")

	def image_preview(self, obj):
		if obj.image:
			return format_html('<img src="{}" style="max-height:60px;max-width:60px;border-radius:8px;box-shadow:0 2px 8px #ff69b4;"/>', obj.image.url)
		return ""
	image_preview.short_description = "Xem trước"

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
	list_display = ("thumbnail", "name", "category", "brand", "price", "quantity_in_stock", "is_active", "is_hot", "num_extra_images")
	list_display_links = ("thumbnail", "name")
	list_editable = ("is_active", "is_hot")
	list_filter = ("category", "brand", "is_active", "is_hot")
	search_fields = ("name", "brand", "category__name", "description")
	list_per_page = 20
	inlines = [ProductImageInline]
	fieldsets = (
		("Thông tin cơ bản", {
			"fields": (
				"name", "category", "brand", "brand_origin", "texture", "skin_type",
				"price", "original_price", "quantity_in_stock", "is_active", "is_hot", "is_promotion",
				"sale_end", "has_gift"
			)
		}),
		("Mô tả & Ảnh", {
			"fields": ("description", "ingredients", "usage", "how_to_use", "image", "image_preview"),
		}),
		("Thời gian", {
			"fields": ("created_at", "updated_at"),
			"classes": ("collapse",)
		}),
	)
	readonly_fields = ("created_at", "updated_at", "image_preview")  # Keep readonly fields

	def get_readonly_fields(self, request, obj=None):
		return super().get_readonly_fields(request, obj)

	def thumbnail(self, obj):
		if obj.image:
			return format_html('<img src="{}" style="max-height:48px;max-width:48px;border-radius:8px;box-shadow:0 2px 8px #ff69b4;"/>', obj.image.url)
		return ""
	thumbnail.short_description = "Ảnh đại diện"

	def image_preview(self, obj):
		if obj.image:
			return format_html('<img src="{}" style="max-height:120px;max-width:120px;border-radius:12px;box-shadow:0 2px 12px #ff69b4;"/>', obj.image.url)
		return ""
	image_preview.short_description = "Xem trước ảnh chính"

	def num_extra_images(self, obj):
		return obj.images.count()
	num_extra_images.short_description = "Số ảnh phụ"




# Đăng ký ProductImage (không cần search)
admin.site.register(ProductImage)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("id", "customer", "order_date", "status", "total_amount")
	search_fields = ("id", "customer__full_name", "customer__email", "shipping_address", "note")
	list_filter = ("status", "order_date")
	date_hierarchy = "order_date"

	actions = ["approve_orders", "mark_as_shipped", "mark_as_completed"]

	def approve_orders(self, request, queryset):
			updated_orders = queryset.filter(status="pending")
			count = updated_orders.update(status="confirmed")
			# Gửi thông báo cho từng khách hàng
			from .models import Notification
			for order in updated_orders:
				if order.customer and hasattr(order.customer, 'user') and order.customer.user:
					Notification.objects.create(
						user=order.customer.user,
						message=f"Đơn hàng #{order.id} của bạn đã được xác nhận và chuyển sang giao vận. Vui lòng theo dõi trạng thái giao hàng!"
					)
			self.message_user(request, f"Đã phê duyệt {count} đơn hàng đang chờ xác nhận và gửi thông báo cho khách hàng.")
	approve_orders.short_description = "Phê duyệt các đơn hàng đang chờ xác nhận và gửi thông báo cho khách hàng"

	def mark_as_shipped(self, request, queryset):
		shipped_orders = queryset.filter(status="confirmed")
		count = shipped_orders.update(status="shipped")
		from .models import Notification
		for order in shipped_orders:
			if order.customer and hasattr(order.customer, 'user') and order.customer.user:
				Notification.objects.create(
					user=order.customer.user,
					message=f"Đơn hàng #{order.id} của bạn đã được giao cho đơn vị vận chuyển. Vui lòng theo dõi trạng thái giao hàng!"
				)
		self.message_user(request, f"Đã chuyển {count} đơn hàng sang trạng thái 'Đã gửi hàng' và gửi thông báo cho khách hàng.")
	mark_as_shipped.short_description = "Chuyển sang trạng thái 'Đã gửi hàng' và gửi thông báo cho khách hàng"

	def mark_as_completed(self, request, queryset):
		completed_orders = queryset.filter(status="shipped")
		count = completed_orders.update(status="completed")
		from .models import Notification
		for order in completed_orders:
			if order.customer and hasattr(order.customer, 'user') and order.customer.user:
				Notification.objects.create(
					user=order.customer.user,
					message=f"Đơn hàng #{order.id} của bạn đã được giao thành công. Cảm ơn bạn đã mua hàng tại Cosmetics!"
				)
		self.message_user(request, f"Đã chuyển {count} đơn hàng sang trạng thái 'Hoàn thành' và gửi thông báo cho khách hàng.")
	mark_as_completed.short_description = "Xác nhận đơn hàng đã giao thành công và gửi thông báo cho khách hàng"

# Tìm kiếm cho Customer
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ("full_name", "email", "phone", "address", "created_at")
	search_fields = ("full_name", "email", "phone", "address")
	list_filter = ("created_at",)

# Tìm kiếm cho Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "description")
	search_fields = ("name", "description")

@admin.register(HotDealBanner)
class HotDealBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", "is_active", "created_at")
    list_editable = ("is_active",)
    search_fields = ("title",)
    list_filter = ("is_active", "created_at")
    readonly_fields = ("created_at", "updated_at", "image_preview")
    fieldsets = (
        (None, {
            "fields": ("title", "image", "image_preview", "link", "is_active")
        }),
        ("Thời gian", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        })
    )
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:80px;max-width:200px;border-radius:8px;box-shadow:0 2px 8px #ff69b4;"/>', obj.image.url)
        return ""
    image_preview.short_description = "Xem trước ảnh"

from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


