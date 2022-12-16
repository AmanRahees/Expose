from .models import Cart,CartItem,Wishlist
from .views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return{}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user, cart_product__is_available=True)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1], cart_product__is_available=True)
            for cart_item in cart_items:
                cart_count += 1
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)

def wishlistCounter(request):
    w_count = 0
    if 'admin' in request.path:
        return{}
    else:
       if request.user.is_authenticated:
            w_items = Wishlist.objects.all().filter(user=request.user,product__is_available=True)
            for w_item in w_items:
                w_count += 1
    return dict(w_count=w_count)

