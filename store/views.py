from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
import json

from .models import Product, Category, Cart, CartItem, Order, OrderItem


# ─── HOME ───────────────────────────────────────────────────────────────────
def home(request):
    featured = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.all()
    all_products = Product.objects.filter(is_active=True)[:12]
    return render(request, 'store/home.html', {
        'featured': featured,
        'categories': categories,
        'all_products': all_products,
    })


# ─── STEP 1: REGISTRATION & LOGIN ───────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        errors = []
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already taken.')
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already registered.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != password2:
            errors.append('Passwords do not match.')

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'store/register.html', {'form_data': request.POST})

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        login(request, user)
        messages.success(request, f'Welcome, {first_name or username}! Your account is ready.')
        return redirect('home')

    return render(request, 'store/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next') or '/'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html', {'next': request.GET.get('next', '')})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ─── STEP 2: PRODUCT PAGES ──────────────────────────────────────────────────
def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if search:
        products = products.filter(name__icontains=search)
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'rating':
        products = products.order_by('-rating')

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search,
        'sort': sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
    })


# ─── STEP 3: CART ────────────────────────────────────────────────────────────
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.select_related('product').all()
    return render(request, 'store/cart.html', {'cart': cart, 'items': items})


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.item_count, 'message': f'{product.name} added to cart!'})
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart')


@login_required
@require_POST
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()
    cart = item.cart if quantity > 0 else Cart.objects.get(user=request.user)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({'success': True, 'cart_total': float(cart.total), 'cart_count': cart.item_count})
    return redirect('cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = item.product.name
    item.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({'success': True, 'cart_total': float(cart.total), 'cart_count': cart.item_count})
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('cart')


# ─── STEP 4: ORDER PROCESSING ────────────────────────────────────────────────
@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.select_related('product').all()
    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    return render(request, 'store/checkout.html', {'cart': cart, 'items': items})


@login_required
@require_POST
def place_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.select_related('product').all()
    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            shipping_name=request.POST.get('full_name', ''),
            shipping_address=request.POST.get('address', ''),
            shipping_city=request.POST.get('city', ''),
            shipping_state=request.POST.get('state', ''),
            shipping_zip=request.POST.get('zip_code', ''),
            shipping_phone=request.POST.get('phone', ''),
            payment_method=request.POST.get('payment_method', 'cod'),
            status='pending',
        )
        total = 0
        for ci in items:
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                quantity=ci.quantity,
                price=ci.product.price,
            )
            total += ci.product.price * ci.quantity
        order.total_price = total
        order.save()
        cart.cartitem_set.all().delete()

    messages.success(request, f'Order #{order.id} placed successfully!')
    return redirect('order_confirmation', order_id=order.id)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})
