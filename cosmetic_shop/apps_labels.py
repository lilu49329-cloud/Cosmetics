from allauth.account.apps import AccountConfig
from allauth.socialaccount.apps import SocialAccountConfig
from django_apscheduler.apps import DjangoApschedulerConfig

class MyAccountConfig(AccountConfig):
    verbose_name = "Xác thực Email"
    def ready(self):
        super().ready()
        from allauth.account.models import EmailAddress
        EmailAddress._meta.verbose_name = "Địa chỉ Email"
        EmailAddress._meta.verbose_name_plural = "Quản lý Địa chỉ Email"

class MySocialAccountConfig(SocialAccountConfig):
    verbose_name = "Mạng xã hội"
    def ready(self):
        super().ready()
        from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
        SocialAccount._meta.verbose_name = "Tài khoản liên kết"
        SocialAccount._meta.verbose_name_plural = "Tài khoản liên kết"
        SocialApp._meta.verbose_name = "Ứng dụng MXH"
        SocialApp._meta.verbose_name_plural = "Ứng dụng MXH"
        SocialToken._meta.verbose_name = "Token ứng dụng"
        SocialToken._meta.verbose_name_plural = "Token ứng dụng"

class MyDjangoApschedulerConfig(DjangoApschedulerConfig):
    verbose_name = "Lịch trình tự động"
    def ready(self):
        super().ready()
        from django_apscheduler.models import DjangoJob, DjangoJobExecution
        DjangoJob._meta.verbose_name = "Công việc định kỳ"
        DjangoJob._meta.verbose_name_plural = "Danh sách Công việc"
        DjangoJobExecution._meta.verbose_name = "Lịch sử chạy"
        DjangoJobExecution._meta.verbose_name_plural = "Lịch sử chạy"
