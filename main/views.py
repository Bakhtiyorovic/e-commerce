from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
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



def Shopping_cart(request):
    return render(request, 'shopping-cart.html')


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

