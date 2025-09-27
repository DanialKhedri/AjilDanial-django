from django.shortcuts import render
from apps.products.models import Product,Category

def home_view(request):

    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    bestsells = Product.objects.filter(categories__slug="bestsell").distinct()[:4]

    context = {
        "title": "خانه",
        "welcome": "به آجیل‌سرا خوش آمدید 🌰",
        "products": products,
        "categories": categories,
        "bestsell": bestsells,
    }

    return render(request, 'home.html', context)
