from django import forms
from .models import Order
from customers.models import Customer

class OrderCreateForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['customer', 'email']
