
from django.urls import path
from . import views
from .password_reset_views import password_reset_request, password_otp_verify, password_reset_confirm
from .chatbot_api import chatbot_api

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/create-now/<int:id>/', views.order_create_now, name='order_create_now'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/created/<int:order_id>/', views.order_created, name='order_created'),
    path('promotions/', views.promotions, name='promotions'),
    path('flash-sale/', views.flash_sale, name='flash_sale'),
    path('flash-sale-list/', views.flash_sale_list, name='flash_sale_list'),
    path('hot-product-list/', views.hot_product_list, name='hot_product_list'),
    path('news/', views.news, name='news'),
    path('brands/', views.brands, name='brands'),
    path('stores/', views.stores, name='stores'),
    path('order-lookup/', views.order_lookup, name='order_lookup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('policy/', views.policy, name='policy'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('products/orders/', views.user_orders, name='user_orders'),
    path('notifications/', views.notifications, name='notifications'),
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    path('avatar-upload/', views.avatar_upload, name='avatar_upload'),
    path('user-update/', views.user_update, name='user_update'),
    path('search/', views.product_search, name='product_search'),
    path('password-reset/', password_reset_request, name='password_reset_request'),
    path('password-reset/otp/', password_otp_verify, name='password_otp_verify'),
    path('password-reset/confirm/', password_reset_confirm, name='password_reset_confirm'),

    # API endpoint cho chatbot
    path('api/chatbot/', chatbot_api, name='chatbot_api'),
]