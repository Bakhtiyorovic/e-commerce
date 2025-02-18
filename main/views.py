from django.shortcuts import render
from .models import *
# Create your views here.

def Home(request):
    return render(request, 'index.html')

def Shop(request):
    return render(request, 'shop.html')

def Shop_details(request):
    return render(request, 'shop-details.html')

def Shopping_cart(request):
    return render(request, 'shopping-cart.html')

def Checkout(request):
    return render(request, 'checkout.html')

def Blog(request):  
    return render(request, 'blog.html')

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

