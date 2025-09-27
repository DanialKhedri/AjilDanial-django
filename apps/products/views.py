from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category


def product_list_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(available=True)

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # مرتب‌سازی: جدیدترین اول
    products = products.order_by('-created_at')

    paginator = Paginator(products, 20)  # صفحه‌بندی 20 تا در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'query': query,
    }
    return render(request, 'product_list.html', context)




# گرفتن تکی یک محصول با اسلاگ
def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)


# گرفتن محصولات بر اساس دسته‌بندی
def products_by_category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(categories=category, available=True)

    paginator = Paginator(products, 20)  # صفحه‌بندی 10 تا در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'category': category,
        
    }
    return render(request, 'product_list.html', context)


# گرفتن همه دسته‌ها
def category_list_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'category_list.html', context)
