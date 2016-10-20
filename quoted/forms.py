from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from .models import Order, Product
from customers.models import Customer
from smart_selects.db_fields import ChainedForeignKey

class OrderCreateForm(forms.ModelForm):
    #customer = forms.ModelChoiceField( queryset= Customer.objects.all() ,
    #                                    widget= forms.TextInput( attrs={'class':'form-control' , 'onfocus':'select()', 'require':'True' } ) )

    email = forms.EmailField( widget= forms.EmailInput( attrs={'class':'form-control' , 'size':'30', 'onfocus':'select()' , 'placeholder':'Email Address'  } ) )
    class Meta:
        model = Order
        fields = ['customer', 'contact', 'email', 'currency', 'paymentterm', 'priceterm', 'quote_sales','ord_date', 'effective_date','comment']
        #raw_id_fields = ('customer',)


class OrderItemForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price']
