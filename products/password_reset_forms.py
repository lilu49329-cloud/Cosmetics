from django import forms
from django.contrib.auth.models import User

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập email đăng ký'}))

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='Mã OTP', max_length=6, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mã OTP'}))

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(label='Mật khẩu mới', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu mới'}))
    confirm_password = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu mới'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Mật khẩu xác nhận không khớp.')
        return cleaned_data
