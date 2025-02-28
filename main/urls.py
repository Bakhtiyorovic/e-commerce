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
]