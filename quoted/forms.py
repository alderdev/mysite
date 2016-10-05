from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from .models import Order
from customers.models import Customer

class OrderCreateForm(forms.ModelForm):
    customer = forms.ModelChoiceField( queryset= Customer.objects.all() ,
                                        widget= forms.TextInput( attrs={'class':'form-control' , 'onfocus':'select()', 'require':'True' } ) )

    email = forms.EmailField( widget= forms.EmailInput( attrs={'class':'form-control' , 'size':'30', 'onfocus':'select()' , 'placeholder':'Email Address'  } ) )
    class Meta:
        model = Order
        fields = ['customer', 'email', 'currency','quote_sales','ord_date', 'effective_date','comment']
        raw_id_fields = ('customer',)
