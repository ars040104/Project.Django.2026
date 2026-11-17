from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product


def product_list(request):
    brand_name = request.GET.get('brand')
    query = request.GET.get('q', '')

    items = Product.objects.all()

    if brand_name:
        items = items.filter(brand=brand_name)

    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query)
        )

    brands = Product.objects.values_list('brand', flat=True).distinct()

    return render(request, 'products/index.html', {
        'items': items,
        'brands': brands,
        'query': query,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def cart_add(request, pk):
    cart = request.session.get('cart', {})
    key = str(pk)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


def cart_remove(request, pk):
    cart = request.session.get('cart', {})
    key = str(pk)
    if key in cart:
        del cart[key]
    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_clear(request):
    request.session['cart'] = {}
    return redirect('cart_detail')