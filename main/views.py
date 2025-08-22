from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from .models import *
import json

# Home page
def Home(request):
    latest_posts = BlogPost.objects.order_by('-date')[:3]
    return render(request, 'index.html', {'latest_posts': latest_posts})

# Shop page
def Shop(request):
    sort_option = request.GET.get('sort', 'default')
    page_number = request.GET.get('page', 1)
    price_range = request.GET.get('price', None)
    search_query = request.GET.get('search', '')

    products = Product.objects.all()

    if search_query:
        products = products.filter(name__icontains=search_query)

    if price_range:
        try:
            min_price, max_price = price_range.split('-')
            if max_price == '+':
                products = products.filter(price__gte=min_price)
            else:
                products = products.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass

    if sort_option == 'low_to_high':
        products = products.order_by('price')
    elif sort_option == 'high_to_low':
        products = products.order_by('-price')

    paginator = Paginator(products, 12)
    paginated_products = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'shop.html', {
        'products': paginated_products,
        'sort_option': sort_option,
        'search_query': search_query,
        'categories': categories,
        'tags': tags,
    })

def FilterByCategory(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'shop.html', {'products': products, 'categories': categories, 'tags': tags})

def FilterByTag(request, tag_id):
    products = Product.objects.filter(tags__id=tag_id)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'shop.html', {'products': products, 'categories': categories, 'tags': tags})

# Shopping Cart
@login_required
def Shopping_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_subtotal = sum(item.total_price() for item in cart_items)
    return render(request, 'shopping-cart.html', {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'cart_total': cart_subtotal
    })

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
@login_required
def update_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cart_items = data.get("cart_items", [])
            cart_subtotal = 0

            for item in cart_items:
                product_id = item.get("product_id")
                quantity = int(item.get("quantity"))
                size = item.get("size", None)

                try:
                    cart_item = Cart.objects.get(product_id=product_id, user=request.user)
                    cart_item.quantity = quantity
                    if size:
                        cart_item.size = size
                    cart_item.save()
                    cart_subtotal += cart_item.total_price()
                except Cart.DoesNotExist:
                    continue  # Cart item mavjud bo'lmasa, davom et

            cart_total = cart_subtotal
            return JsonResponse({"cart_subtotal": cart_subtotal, "cart_total": cart_total, "success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

# Checkout
@login_required
def Checkout(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        country = request.POST.get("country")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        order_notes = request.POST.get("order_notes")

        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            country=country,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            email=email,
            order_notes=order_notes,
        )

        # Cart itemsni OrderItemga ko'chirish
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                size=item.size
            )
        # Cartni bo'shatish
        cart_items.delete()

        return redirect("orders_list")

    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, "checkout.html", {'cart_items': cart_items, 'total_price': total_price})

# Blog
def Blog(request):
    blog_posts = BlogPost.objects.all().order_by('-date')
    return render(request, 'blog.html', {'blog_posts': blog_posts})

def Blog_details(request):
    return render(request, 'blog-details.html')

def About(request):
    return render(request, 'about.html')

# Contact
def Contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            return render(request, 'contact.html', {'message': 'Data saved successfully.'})
        else:
            return render(request, 'contact.html', {'error': 'Please fill in all fields.'})
    return render(request, 'contact.html')

# Newsletter
def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "You have successfully subscribed!")
            else:
                messages.warning(request, "This email is already subscribed.")
        else:
            messages.error(request, "Please enter a valid email address.")
    return redirect(request.META.get("HTTP_REFERER", "/"))

# Orders
@login_required
def OrdersList(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "order_list.html", {'orders': orders})

@login_required
def orders_api(request):
    try:
        orders_list = Order.objects.filter(user=request.user).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(orders_list, 5)
        orders = paginator.get_page(page)

        data = []
        for order in orders:
            items_data = [
                {
                    "product_name": item.product.name,
                    "price": float(item.product.price),
                    "quantity": item.quantity,
                    "size": item.size
                } for item in order.items.all()
            ]
            data.append({
                "order_id": order.id,
                "total_price": float(order.total_price()),
                "items": items_data
            })

        return JsonResponse({
            "orders": data,
            "has_next": orders.has_next(),
            "has_previous": orders.has_previous(),
            "num_pages": paginator.num_pages,
            "current_page": orders.number
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
