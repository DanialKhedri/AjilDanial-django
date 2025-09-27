from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "get_categories", "product_type", "available", "created_at")
    list_filter = ("product_type", "available", "categories")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("categories",)  # برای انتخاب راحت‌تر دسته‌بندی‌ها

    def get_categories(self, obj):
        """نمایش دسته‌ها به صورت لیست در ادمین"""
        return "، ".join([c.name for c in obj.categories.all()])

    get_categories.short_description = "دسته‌بندی‌ها"
