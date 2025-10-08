
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from products.views import user_login
from products.admin_global_search import admin_global_search

urlpatterns = [
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/login/')),
    path('admin/search/', admin_global_search, name='admin_global_search'),
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/', __import__('products.views').views.register, name='register'),
    path('accounts/', include('allauth.urls')),  # allauth
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
