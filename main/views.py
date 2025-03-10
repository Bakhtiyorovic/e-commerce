from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# Create your views here.

def Home(request):
    return render(request, 'index.html')


def Shop(request):
    sort_option = request.GET.get('sort', 'default')  # URL'dan tartiblash parametrini olish
    page_number = request.GET.get('page', 1)  # URL'dan sahifa raqamini olish (default: 1)

    # Saralash opsiyalarini qo‘llash
    if sort_option == 'low_to_high':
        products = Product.objects.all().order_by('price')
    elif sort_option == 'high_to_low':
        products = Product.objects.all().order_by('-price')
    else:
        products = Product.objects.all()

    # Sahifalashni qo‘llash (har bir sahifada 12 ta mahsulot)
    paginator = Paginator(products, 12)
    paginated_products = paginator.get_page(page_number)

    return render(request, 'shop.html', {
        'products': paginated_products,
        'sort_option': sort_option
    })


@login_required
def Shopping_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_subtotal = sum(item.total_price() for item in cart_items)
    return render(request, 'shopping-cart.html',
                  {'cart_items': cart_items, 'cart_subtotal': cart_subtotal, 'cart_total': cart_subtotal})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shopping_cart')


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('shopping_cart')


@csrf_exempt
def update_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cart_items = data.get("cart_items", [])
            cart_subtotal = 0

            for item in cart_items:
                product_id = item.get("product_id")
                quantity = int(item.get("quantity"))

                cart_item = Cart.objects.get(product_id=product_id, user=request.user)
                cart_item.quantity = quantity
                cart_item.save()

                cart_subtotal += cart_item.product.price * quantity

            cart_total = cart_subtotal  # Agar soliq yoki chegirma bo‘lsa, shu yerda qo‘shish mumkin

            return JsonResponse({"cart_subtotal": cart_subtotal, "cart_total": cart_total})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)





def Checkout(request):
    return render(request, 'checkout.html')


def Blog(request):
    blog_posts = BlogPost.objects.all().order_by('-date')
    return render(request, 'blog.html', {'blog_posts': blog_posts})


def Blog_details(request):
    return render(request, 'blog-details.html')


def About(request): 
    return render(request, 'about.html')


def Contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            contact_data = ContactMessage(name=name, email=email, message=message)
            contact_data.save()
            return render(request, 'contact.html', {'message': 'Data saved successfully.'})
        else:
            return render(request, 'contact.html', {'error': 'Please fill in all fields..'})
    else:
        return render(request, 'contact.html')

