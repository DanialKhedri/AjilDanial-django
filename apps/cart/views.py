from django.shortcuts import render, get_object_or_404, redirect
from apps.products.models import Product

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if product.product_type == "bulk":
        weight = float(request.POST.get('weight', 100))  # پیش‌فرض 100 گرم
        quantity = weight / 1000  # تبدیل گرم به کیلوگرم
        price = float(product.price_per_kg)
    else:
        quantity = int(request.POST.get('quantity', 1))  # پیش‌فرض 1 بسته
        price = float(product.package_price)

    product_id_str = str(product.id)

    # بررسی وجود محصول و اصلاح کلیدها برای جلوگیری از KeyError
    if product_id_str in cart:
        cart_item = cart[product_id_str]
        cart_item['quantity'] = float(cart_item.get('quantity', 0)) + quantity
        cart_item['price'] = float(cart_item.get('price', price))
    else:
        cart[product_id_str] = {
            'title': product.title,
            'price': price,
            'quantity': quantity,
            'type': product.product_type
        }

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})

    # محاسبه جمع هر آیتم
    for item in cart.values():
        item['total'] = float(item.get('price', 0)) * float(item.get('quantity', 0))

    # جمع کل کل سبد
    total = sum(item['total'] for item in cart.values()) if cart else 0

    empty = not bool(cart)

    return render(request, 'cart.html', {
        'cart': cart,
        'total': total,
        'empty': empty
    })
