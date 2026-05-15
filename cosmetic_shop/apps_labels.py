from allauth.account.apps import AccountConfig
from allauth.socialaccount.apps import SocialAccountConfig
from django_apscheduler.apps import DjangoApschedulerConfig
from django.contrib.auth.apps import AuthConfig

class MyAccountConfig(AccountConfig):
    verbose_name = "Xác thực Email"
    def ready(self):
        super().ready()
        try:
            from allauth.account.models import EmailAddress
            EmailAddress._meta.verbose_name = "Địa chỉ Email"
            EmailAddress._meta.verbose_name_plural = "Quản lý Địa chỉ Email"
        except (ImportError, RuntimeError):
            pass

class MySocialAccountConfig(SocialAccountConfig):
    verbose_name = "Mạng xã hội"
    def ready(self):
        super().ready()
        try:
            from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
            SocialAccount._meta.verbose_name = "Tài khoản liên kết"
            SocialAccount._meta.verbose_name_plural = "Tài khoản liên kết"
            SocialApp._meta.verbose_name = "Ứng dụng MXH"
            SocialApp._meta.verbose_name_plural = "Ứng dụng MXH"
            SocialToken._meta.verbose_name = "Token ứng dụng"
            SocialToken._meta.verbose_name_plural = "Token ứng dụng"
        except (ImportError, RuntimeError):
            pass

class MyDjangoApschedulerConfig(DjangoApschedulerConfig):
    verbose_name = "Lịch trình tự động"
    def ready(self):
        super().ready()
        try:
            from django_apscheduler.models import DjangoJob, DjangoJobExecution
            DjangoJob._meta.verbose_name = "Công việc định kỳ"
            DjangoJob._meta.verbose_name_plural = "Danh sách Công việc"
            DjangoJobExecution._meta.verbose_name = "Lịch sử chạy"
            DjangoJobExecution._meta.verbose_name_plural = "Lịch sử chạy"
        except (ImportError, RuntimeError):
            pass

class MyAuthConfig(AuthConfig):
    verbose_name = "Xác thực và Ủy quyền"
    def ready(self):
        super().ready()
        try:
            from django.contrib.auth.models import User, Group
            User._meta.verbose_name = "Người sử dụng"
            User._meta.verbose_name_plural = "Danh sách Người dùng"
            Group._meta.verbose_name = "Nhóm người dùng"
            Group._meta.verbose_name_plural = "Quản lý Nhóm"
        except (ImportError, RuntimeError):
            pass
