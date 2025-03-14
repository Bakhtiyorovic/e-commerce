from django import forms
from .models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "country", "address", "city", "state", "zip_code", "phone", "email", "order_notes"]
