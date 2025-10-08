from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.db.models import Q
from products.models import Product, Order, Customer, Category

@staff_member_required
def admin_global_search(request):
    query = request.GET.get('q', '').strip()
    product_results = order_results = customer_results = category_results = []
    if query:
        product_results = Product.objects.filter(
            Q(name__icontains=query) | Q(brand__icontains=query) | Q(description__icontains=query)
        )
        order_results = Order.objects.filter(
            Q(id__icontains=query) | Q(customer__full_name__icontains=query) | Q(note__icontains=query)
        )
        customer_results = Customer.objects.filter(
            Q(full_name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query)
        )
        category_results = Category.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'admin/global_search_results.html', {
        'query': query,
        'product_results': product_results,
        'order_results': order_results,
        'customer_results': customer_results,
        'category_results': category_results,
    })
