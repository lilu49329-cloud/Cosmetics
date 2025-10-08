from django import forms
from .models import Product, Category, Customer, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'description', 'price', 'quantity_in_stock', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ProductSearchForm(forms.Form):
    query = forms.CharField(
        label='Tìm kiếm',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nhập tên hoặc thương hiệu...'})
    )
    category = forms.ModelChoiceField(
        label='Danh mục',
        queryset=Category.objects.all(),
        required=False,
        empty_label='-- Tất cả danh mục --'
    )
    min_price = forms.DecimalField(label='Giá từ', required=False, min_value=0, decimal_places=0, widget=forms.NumberInput(attrs={'placeholder': 'Từ giá...'}))
    max_price = forms.DecimalField(label='Đến', required=False, min_value=0, decimal_places=0, widget=forms.NumberInput(attrs={'placeholder': 'Đến giá...'}))
    brand = forms.CharField(label='Thương hiệu', required=False, widget=forms.TextInput(attrs={'placeholder': 'Thương hiệu...'}))
    sort_by = forms.ChoiceField(
        label='Sắp xếp',
        required=False,
        choices=[
            ('', '---'),
            ('price_asc', 'Giá tăng dần'),
            ('price_desc', 'Giá giảm dần'),
            ('name_asc', 'Tên A-Z'),
            ('name_desc', 'Tên Z-A'),
            ('newest', 'Mới nhất'),
        ]
    )

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        label='Số lượng',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )

class OrderForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        label='Hình thức thanh toán',
        choices=Order.PAYMENT_METHODS,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = Order
        fields = ['shipping_address', 'note', 'payment_method']
        widgets = {
            'shipping_address': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'email', 'phone', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
