from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from .password_reset_forms import PasswordResetRequestForm, OTPVerificationForm, PasswordResetForm

# Simple in-memory store for OTPs (for demo; use cache/db in production)
OTP_STORE = {}

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = get_random_string(length=6, allowed_chars='0123456789')
                OTP_STORE[email] = otp
                send_mail(
                    'Mã OTP khôi phục mật khẩu',
                    f'Mã OTP của bạn là: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                request.session['reset_email'] = email
                messages.success(request, 'Mã OTP đã được gửi về email của bạn.')
                return redirect('password_otp_verify')
            except User.DoesNotExist:
                form.add_error('email', 'Email không tồn tại trong hệ thống.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'products/password_reset_request.html', {'form': form})

def password_otp_verify(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('password_reset_request')
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if OTP_STORE.get(email) == otp:
                messages.success(request, 'Xác thực OTP thành công. Đặt lại mật khẩu mới.')
                return redirect('password_reset_confirm')
            else:
                form.add_error('otp', 'Mã OTP không đúng hoặc đã hết hạn.')
    else:
        form = OTPVerificationForm()
    return render(request, 'products/password_otp_verify.html', {'form': form})

def password_reset_confirm(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('password_reset_request')
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                user = User.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                OTP_STORE.pop(email, None)
                request.session.pop('reset_email', None)
                messages.success(request, 'Mật khẩu đã được đặt lại thành công. Bạn có thể đăng nhập.')
                return redirect('login')
            except User.DoesNotExist:
                form.add_error(None, 'Không tìm thấy người dùng.')
    else:
        form = PasswordResetForm()
    return render(request, 'products/password_reset_confirm.html', {'form': form})
