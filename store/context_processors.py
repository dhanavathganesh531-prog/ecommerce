from .models import Cart, Category


def cart_context(request):
    """Context processor providing cart items count and categories across all templates."""
    cart_count = 0
    categories = Category.objects.all()

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                cart = None
            else:
                cart = Cart.objects.filter(session_key=session_key).first()

        if cart:
            cart_count = cart.get_total_items()
    except Exception:
        cart_count = 0

    return {
        'cart_item_count': cart_count,
        'nav_categories': categories,
    }
