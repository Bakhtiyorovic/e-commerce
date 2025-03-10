from .views import *
from django.urls import path

urlpatterns = [
    path('', Home, name= 'home'),
    path('blog/', Blog, name= 'blog'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('shop/', Shop, name= 'shop'),
    path('shopping_cart/', Shopping_cart, name= 'shopping_cart'),
    path('checkout/', Checkout, name= 'checkout'),
    path('blog_details/', Blog_details, name= 'blog_details'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path("update-cart/", update_cart, name="update_cart"),
]