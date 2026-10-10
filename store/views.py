from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from decimal import Decimal

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .forms import UserRegisterForm, CheckoutForm


def _get_cart(request):
    """Helper function to fetch or create a shopping cart for the current session/user."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def home(request):
    """Store homepage with featured products and categories."""
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    latest_products = Product.objects.filter(is_available=True)[:8]
    categories = Category.objects.all()

    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def product_list(request, category_slug=None):
    """Product catalog with category filter, search, and sorting."""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Search keyword
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Sort options
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': query or '',
        'selected_sort': sort or '',
    }
    return render(request, 'products.html', context)


def product_detail(request, slug):
    """Detailed view for a single product."""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


def cart_view(request):
    """Shopping cart overview with line items and subtotal."""
    cart = _get_cart(request)
    cart_items = cart.items.select_related('product').all()
    subtotal = cart.get_subtotal()
    shipping = Decimal('0.00') if subtotal >= 50 or subtotal == 0 else Decimal('9.99')
    total = subtotal + shipping

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    """Add a product to cart or increment quantity."""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = _get_cart(request)

    quantity = 1
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    messages.success(request, f'Added "{product.name}" to your cart.')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'store:cart'
    return redirect(next_url)


def remove_from_cart(request, product_id):
    """Decrease item quantity by 1 in cart, or delete if 0."""
    cart = _get_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    messages.info(request, f'Updated quantity for "{cart_item.product.name}".')
    return redirect('store:cart')


def delete_from_cart(request, product_id):
    """Completely remove an item from the cart."""
    cart = _get_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    product_name = cart_item.product.name
    cart_item.delete()

    messages.warning(request, f'Removed "{product_name}" from your cart.')
    return redirect('store:cart')


def checkout_view(request):
    """Checkout page to place an order."""
    cart = _get_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items:
        messages.warning(request, 'Your cart is empty. Add products before checking out.')
        return redirect('store:products')

    subtotal = cart.get_subtotal()
    shipping = Decimal('0.00') if subtotal >= 50 or subtotal == 0 else Decimal('9.99')
    total = subtotal + shipping

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_amount = total
            order.save()

            # Create OrderItems from cart
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.get_display_price(),
                    quantity=item.quantity,
                )

            # Clear cart
            cart.items.all().delete()

            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('store:order_success', order_id=order.id)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
            }
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'checkout.html', context)


def order_success(request, order_id):
    """Display order confirmation."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})


def register_view(request):
    """Handle new user registration."""
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('store:home')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Handle user login and migrate any guest cart items."""
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Check guest session cart before logging in
            guest_session_key = request.session.session_key
            login(request, user)

            # Migrate guest items to user cart if any exist
            if guest_session_key:
                guest_cart = Cart.objects.filter(session_key=guest_session_key).first()
                if guest_cart and guest_cart.items.exists():
                    user_cart, _ = Cart.objects.get_or_create(user=user)
                    for item in guest_cart.items.all():
                        existing_item, created = CartItem.objects.get_or_create(
                            cart=user_cart,
                            product=item.product,
                            defaults={'quantity': item.quantity}
                        )
                        if not created:
                            existing_item.quantity += item.quantity
                            existing_item.save()
                    guest_cart.delete()

            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next') or 'store:home'
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('store:home')
