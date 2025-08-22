from .views import *
from django.urls import path
from . import views

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
    path('shop/category/<int:category_id>/', FilterByCategory, name='filter_by_category'),
    path('shop/tag/<int:tag_id>/', FilterByTag, name='filter_by_tag'),
    path("subscribe/", subscribe_newsletter, name="subscribe_newsletter"),
    path('orders/', views.OrdersList, name='orders_list'),
    path('api/orders/', views.orders_api, name='orders_api'),
]