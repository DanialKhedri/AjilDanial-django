from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
import re

# کلاس مدیریت کاربر: مسئول ساخت کاربر معمولی و ادمین
class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('شماره تلفن الزامی است')

        if self.model.objects.filter(phone_number=phone_number).exists():
            raise ValueError('این شماره تلفن قبلاً ثبت شده است')

        if not re.fullmatch(r'09\d{9}', phone_number):
            raise ValueError('شماره موبایل باید با 09 شروع شود و دقیقاً 11 رقم باشد')

        if not password or len(password) < 8 or len(password) > 50:
            raise ValueError('رمز عبور باید بین ۸ تا ۵۰ کاراکتر باشد')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

# مدل اصلی کاربر سفارشی
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    # اعتبارسنجی مدل قبل از ذخیره
    def clean(self):
        if not re.fullmatch(r'09\d{9}', self.phone_number):
            raise ValidationError("شماره موبایل باید با 09 شروع شود و دقیقاً 11 رقم باشد")

        # هش شده بودن رمز عبور باعث می‌شه این چک فقط در شرایط خاص کاربرد داشته باشه
        if self.password and (len(self.password) < 8 or len(self.password) > 50):
            raise ValidationError("رمز عبور باید بین ۸ تا ۵۰ کاراکتر باشد")
