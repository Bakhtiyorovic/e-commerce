from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Cart  # O'zingizning modelingiz nomini tekshiring

def cart_total(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart)
    else:
        total_price = 0.00  # Agar foydalanuvchi login qilmagan bo‘lsa

    return {"cart_total_price": total_price}
