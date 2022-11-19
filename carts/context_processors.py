from .models import Carts, CartItem
from .views import _cart_id


# Create Carts items notification

def counter(request):
    cart_count = 0
    if 'admin ' in request.path:
        return {}
    else:
        try:
            cart = Carts.objects.filter(cart_id=_cart_id(request))
            cart_item = CartItem.objects.all().filter(carts=cart[:1])
            for cart_item in cart_item:
                cart_count += cart_item.quantity
        except Carts.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
