# context_processors.py

from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = len(cart_items)
    else:
        cart_count = 0
    
    return {'cart_count': cart_count}
