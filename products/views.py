from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Customer, Order, OrderItem, Notification, HotDealBanner, UserProfile
from .forms import ProductForm, ProductSearchForm, CartAddProductForm, CustomerForm, OrderForm
from .cart import Cart
from django.utils import timezone

@login_required
def user_update(request):
    if request.method == 'POST':
        user = request.user
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        # Cập nhật tên
        if full_name:
            user.first_name = full_name

        # Cập nhật email nếu thay đổi và không trùng email khác
        if email and email != user.email:
            # Kiểm tra email đã tồn tại chưa
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if not User.objects.filter(email=email).exclude(pk=user.pk).exists():
                user.email = email
        user.save()

        # Cập nhật số điện thoại
        if hasattr(user, 'profile'):
            user.profile.phone = phone
            user.profile.save()

        return redirect('user_dashboard')
from django.http import JsonResponse
from .models import Notification

# API trả về danh sách thông báo cho người dùng hiện tại
from django.contrib.auth.decorators import login_required
@login_required
def notifications_api(request):
    notifications = []
    user = request.user
    if user.is_authenticated:
        notifications_qs = Notification.objects.filter(user=user).order_by('-created_at')[:10]
        notifications = [
            {
                'message': n.message,
                'created_at': n.created_at.strftime('%d/%m/%Y %H:%M'),
                'is_read': n.is_read
            }
            for n in notifications_qs
        ]
    return JsonResponse({'notifications': notifications})
from django.views.decorators.http import require_POST
from .models import HotDealBanner

# Đặt hàng ngay 1 sản phẩm (không qua giỏ hàng)
@require_POST
def order_create_now(request, id):
    product = get_object_or_404(Product, id=id)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (TypeError, ValueError):
        quantity = 1
    # Tạo customer tạm nếu chưa đăng nhập
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(email=request.user.email, defaults={
            'full_name': request.user.get_full_name() or request.user.username
        })
    else:
        # Có thể yêu cầu nhập thông tin khách hàng ở bước tiếp theo
        customer = None
    # Tạo đơn hàng
    order = Order.objects.create(customer=customer)
    OrderItem.objects.create(order=order, product=product, product_name=product.name, price=product.price, quantity=quantity)
    order.calculate_total()
    # Chuyển đến trang chi tiết đơn hàng
    return redirect('order_detail', order_id=order.id)
from django.utils import timezone

# View for hot product list
def hot_product_list(request):
    products = Product.objects.filter(is_hot=True, is_active=True)
    categories = Category.objects.all()
    from django.utils import timezone
    now = timezone.now()
    flash_sale_products = Product.objects.filter(is_active=True, sale_end__gt=now)
    return render(request, 'products/hot_product_list.html', {
        'products': products,
        'categories': categories,
        'flash_sale_products': flash_sale_products,
    })
from django.utils import timezone

def flash_sale_list(request):
    from django.utils import timezone
    now = timezone.now()
    products_qs = Product.objects.filter(is_active=True, is_promotion=True, sale_end__gt=now)
    products = []
    for product in products_qs:
        sale_end = getattr(product, 'sale_end', None)
        if product.original_price and product.original_price > product.price:
            discount_percent = int(round((product.original_price - product.price) / product.original_price * 100))
        else:
            discount_percent = 0
        products.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'image': product.image,
            'price': product.price,
            'original_price': product.original_price,
            'has_gift': getattr(product, 'has_gift', False),
            'is_gift': getattr(product, 'is_gift', False),
            'sale_end': sale_end,
            'discount_percent': discount_percent,
            'description': getattr(product, 'description', ''),
        })
    # Lấy các banner hot deals đang active
    hotdeal_banners = HotDealBanner.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, 'products/flash_sale_list.html', {
        'products': products,
        'categories': categories,
        'hotdeal_banners': hotdeal_banners,
    })
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Product, Category, Customer, Order, OrderItem
from .forms import ProductForm, ProductSearchForm, CartAddProductForm, CustomerForm, OrderForm
from .cart import Cart
from django.contrib.auth.decorators import login_required

# Thêm sản phẩm vào giỏ hàng
from django.views.decorators.http import require_POST

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # Nếu là AJAX (fetch), luôn trả về JSON kể cả khi lỗi
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Bạn chưa đăng nhập.'}, status=403)
        try:
            cart.add(product=product, quantity=1, override_quantity=False)
            from .models import Notification
            Notification.objects.create(user=request.user, message=f'Đã thêm {product.name} vào giỏ hàng!')
            notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
            cart_count = len(cart)
            return JsonResponse({'success': True, 'notifications_count': notifications_count, 'cart_count': cart_count})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    # Nếu không phải AJAX thì xử lý như cũ
    cart.add(product=product, quantity=1, override_quantity=False)
    messages.success(request, f'Đã thêm {product.name} vào giỏ hàng!')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

# Trang mở rộng
def promotions(request):
    promotions = [
        {'title': 'Giảm giá 50%', 'desc': 'Áp dụng cho đơn từ 500k'},
        {'title': 'Mua 1 tặng 1', 'desc': 'Chỉ áp dụng cho sản phẩm dưỡng da'},
    ]
    return render(request, 'products/promotions.html', {'promotions': promotions})

from django.shortcuts import redirect

def flash_sale(request):
    # Redirect to the real flash sale list page
    return redirect('flash_sale_list')

def news(request):
    news_list = [
        {'title': 'Ra mắt sản phẩm mới', 'content': 'Chi tiết về sản phẩm mới...'},
    ]
    return render(request, 'products/news.html', {'news_list': news_list})

def brands(request):
    from .models import Brand
    brands = Brand.objects.all().order_by('name')
    return render(request, 'products/brands.html', {'brands': brands})

def stores(request):
    from .models import Store
    stores_qs = Store.objects.all()
    stores = []
    for store in stores_qs:
        # Tạo link chỉ đường Google Maps
        map_query = store.address.replace(' ', '+')
        map_url = f'https://www.google.com/maps/search/?api=1&query={map_query}'
        stores.append({
            'name': store.name,
            'address': store.address,
            'phone': store.phone,
            'map_url': map_url
        })
    return render(request, 'products/stores.html', {'stores': stores})

def order_lookup(request):
    orders = None
    if request.method == 'POST':
        code = request.POST.get('order_code')
        if code == '123':
            orders = [{'code': '123', 'status': 'Đang giao'}]
        else:
            orders = []
    return render(request, 'products/order_lookup.html', {'orders': orders})

# Trang giới thiệu
def about(request):
    return render(request, 'products/about.html')

# Trang liên hệ
def contact(request):
    return render(request, 'products/contact.html')

# Trang chính sách
def policy(request):
    return render(request, 'products/policy.html')
# Quản lý đơn hàng cho admin/người bán
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='/login/')
def admin_order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'products/admin_order_list.html', {'orders': orders})

@staff_member_required(login_url='/login/')
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status and new_status != order.status:
            old_status = order.status
            order.status = new_status
            order.save()
            # Gửi thông báo cho khách hàng khi trạng thái thay đổi
            if order.customer and hasattr(order.customer, 'user') and order.customer.user:
                from .models import Notification
                if new_status == 'confirmed':
                    msg = f"Đơn hàng #{order.id} của bạn đã được xác nhận và chuyển sang giao vận. Vui lòng theo dõi trạng thái giao hàng!"
                elif new_status == 'shipped':
                    msg = f"Đơn hàng #{order.id} của bạn đã được giao cho đơn vị vận chuyển. Vui lòng theo dõi trạng thái giao hàng!"
                elif new_status == 'completed':
                    msg = f"Đơn hàng #{order.id} của bạn đã được giao thành công. Cảm ơn bạn đã mua hàng tại Cosmetics!"
                elif new_status == 'canceled':
                    msg = f"Đơn hàng #{order.id} của bạn đã bị hủy. Nếu có thắc mắc, vui lòng liên hệ hỗ trợ."
                else:
                    msg = f"Trạng thái đơn hàng #{order.id} đã được cập nhật: {order.get_status_display()}"
                Notification.objects.create(user=order.customer.user, message=msg)
            messages.success(request, f'Trạng thái đơn hàng #{order.id} đã được cập nhật thành "{order.get_status_display()}".')
            return redirect('admin_order_detail', order_id=order.id)
    return render(request, 'products/admin_order_detail.html', {'order': order})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Product, Category, Customer, Order, OrderItem
from .forms import ProductForm, ProductSearchForm, CartAddProductForm, CustomerForm, OrderForm
from .cart import Cart
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def home(request):
    products = Product.objects.all().order_by('-created_at')[:9]
    categories = Category.objects.all()
    hot_products = Product.objects.filter(is_hot=True, is_active=True)[:8]
    from django.utils import timezone
    now = timezone.now()
    flash_sale_products_qs = Product.objects.filter(is_active=True, is_promotion=True, sale_end__gt=now)
    flash_sale_products = []
    for product in flash_sale_products_qs:
        if product.original_price and product.original_price > product.price:
            discount_percent = int(round((product.original_price - product.price) / product.original_price * 100))
        else:
            discount_percent = 0
        flash_sale_products.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'image': product.image,
            'price': product.price,
            'original_price': product.original_price,
            'has_gift': getattr(product, 'has_gift', False),
            'is_gift': getattr(product, 'is_gift', False),
            'sale_end': getattr(product, 'sale_end', None),
            'discount_percent': discount_percent,
        })
    cart = Cart(request)
    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories,
        'hot_products': hot_products,
        'flash_sale_products': flash_sale_products,
        'cart': cart,
    })

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {'products': products, 'categories': categories})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    form = CartAddProductForm()
    discount_amount = None
    discount_percent = None
    if product.original_price and product.original_price > product.price:
        discount_amount = product.original_price - product.price
        discount_percent = round(100 * (product.original_price - product.price) / product.original_price)
    return render(request, 'products/product_detail.html', {
        'product': product,
        'form': form,
        'discount_amount': discount_amount,
        'discount_percent': discount_percent,
        # 'recommended_products': [],
    })

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Sản phẩm "{product.name}" đã được tạo thành công!')
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Thêm sản phẩm mới'
    })

def product_edit(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sản phẩm "{product.name}" đã được cập nhật!')
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'product': product,
        'title': 'Chỉnh sửa sản phẩm'
    })

def product_delete(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Sản phẩm "{product_name}" đã được xóa!')
        return redirect('products')

    return render(request, 'products/product_confirm_delete.html', {'product': product})

# Chức năng giỏ hàng
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'products/cart.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

# Chức năng đặt hàng
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('products')

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        order_form = OrderForm(request.POST)

        if customer_form.is_valid() and order_form.is_valid():
            try:
                customer = Customer.objects.get(email=customer_form.cleaned_data['email'])
                customer_form = CustomerForm(request.POST, instance=customer)
                customer = customer_form.save()
            except Customer.DoesNotExist:
                customer = customer_form.save()

            order = order_form.save(commit=False)
            order.customer = customer
            order.payment_method = order_form.cleaned_data['payment_method']
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    price=item['price'],
                    quantity=item['quantity']
                )

            order.calculate_total()

            cart.clear()

            # Gửi notification cho user nếu đã đăng nhập
            if request.user.is_authenticated:
                from .models import Notification
                Notification.objects.create(
                    user=request.user,
                    message=f'Bạn đã đặt hàng thành công! Mã đơn hàng: #{order.id}'
                )

            # Chuyển hướng sang trang thành công với nút xem chi tiết đơn
            return redirect('order_created', order_id=order.id)
    else:
        customer_form = CustomerForm()
        order_form = OrderForm()

    return render(request, 'products/orders/create.html', {
        'cart': cart,
        'customer_form': customer_form,
        'order_form': order_form
    })
def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'products/orders/created.html', {'order': order})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'products/orders/detail.html', {'order': order})

# Chức năng người dùng
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'products/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Nếu là admin/staff thì vào /admin/
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('home')
        else:
            messages.error(request, "Sai tài khoản hoặc mật khẩu!")
    else:
        form = AuthenticationForm()
    return render(request, 'products/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_dashboard(request):
    return render(request, 'products/user_dashboard.html')

@login_required
def user_orders(request):
    try:
        customer = Customer.objects.get(email=request.user.email)
        orders = Order.objects.filter(customer=customer).order_by('-order_date')
    except Customer.DoesNotExist:
        orders = []
    return render(request, 'products/user_orders.html', {'orders': orders})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def avatar_upload(request):
    from django.contrib import messages
    if request.method == 'POST':
        avatar_file = request.FILES.get('avatar')
        if avatar_file:
            profile = request.user.profile
            profile.avatar = avatar_file
            profile.save()
            messages.success(request, 'Ảnh đại diện đã được cập nhật thành công!')
        else:
            messages.error(request, 'Vui lòng chọn ảnh để tải lên.')
    return redirect('user_dashboard')

def product_search(request):
    query = request.GET.get('q', '').strip()
    products = []
    categories = Category.objects.all()
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        ).distinct()
    return render(request, 'products/product_search_results.html', {
        'query': query,
        'products': products,
        'categories': categories,
    })

from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    # Đánh dấu tất cả là đã đọc khi truy cập
    notifications.update(is_read=True)
    return render(request, 'products/notifications.html', {'notifications': notifications})