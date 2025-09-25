from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته")
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = (
        ("bulk", "فله‌ای"),
        ("packaged", "بسته‌بندی"),
    )

    title = models.CharField(max_length=150, verbose_name="عنوان محصول")
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="تصویر محصول")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES, default="bulk", verbose_name="نوع محصول")

    # برای محصولات فله‌ای
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="قیمت هر کیلو")

    # برای محصولات بسته‌بندی
    package_weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="وزن بسته (گرم)")
    package_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="قیمت بسته")

    available = models.BooleanField(default=True, verbose_name="موجودی")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)