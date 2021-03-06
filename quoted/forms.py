from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from .models import Order, Product, OrderItem
from customers.models import Customer
from smart_selects.db_fields import ChainedForeignKey
from django.contrib import admin
from django.utils import timezone

class OrderCreateForm(forms.ModelForm):
    customer = forms.ModelChoiceField( queryset= Customer.objects.all() ,
                                        widget= forms.TextInput( attrs={'class':'form-control' , 'onfocus':'select()', 'require':'True' } ) )
    effective_date = forms.DateField( initial= timezone.now() + timezone.timedelta(days=30),
                            widget= forms.DateInput( attrs={'class':'form-control' , 'onfocus':'select()', 'require':'True' } ))

    #email = forms.EmailField( widget= forms.EmailInput( attrs={'class':'form-control' , 'size':'30', 'onfocus':'select()' , 'placeholder':'Email Address'  } ) )
    class Meta:
        model = Order
        fields = ['customer', 'contact', 'currency', 'paymentterm', 'priceterm', 'quote_user','ord_date', 'effective_date','comment']
        raw_id_fields = ['customer']
        widgets = {
            'contact': forms.Select(attrs={ 'class':'form-control'}),
            #'email': forms.EmailInput(attrs={ 'class':'form-control','onfocus':'select()'}),
            'currency': forms.Select(attrs={ 'class':'form-control'}),
            'paymentterm': forms.Select(attrs={ 'class':'form-control'}),
            'priceterm': forms.Select(attrs={ 'class':'form-control'}),
            'quote_sales': forms.TextInput(attrs={ 'class':'form-control'}),
            'ord_date': forms.DateInput(attrs={ 'class':'form-control'}),
            'effective_date': forms.DateInput(attrs={ 'class':'form-control'}),
            'comment': forms.Textarea(attrs={ 'class':'form-control'}),
            'quote_user':forms.HiddenInput(attrs={ 'class':'form-control'}),
        }


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['is_valid','customer', 'currency', 'paymentterm', 'priceterm', 'quote_sales','ord_date', 'effective_date','comment']
        raw_id_fields = ['customer']
        widgets = {
            'customer': forms.TextInput(attrs={ 'class':'form-control', 'readonly':'readonly'}),
            #'email': forms.EmailInput(attrs={ 'class':'form-control'}),
            'currency': forms.Select(attrs={ 'class':'form-control'}),
            'paymentterm': forms.Select(attrs={ 'class':'form-control'}),
            'priceterm': forms.Select(attrs={ 'class':'form-control'}),
            'quote_sales': forms.TextInput(attrs={ 'class':'form-control'}),
            'ord_date': forms.DateInput(attrs={ 'class':'form-control'}),
            'effective_date': forms.DateInput(attrs={ 'class':'form-control'}),
            'comment': forms.Textarea(attrs={ 'class':'form-control'}),
        }



class OrderItemForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name']


class OrderItemUpdateForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = ['orderitem_name','orderitem_modelname']
        #exclude = ( 'orderitem_height_field','orderitem_width_field')
        widgets = {
            'customer': forms.TextInput(attrs={ 'class':'form-control', 'readonly':'readonly'}),
            #'email': forms.EmailInput(attrs={ 'class':'form-control'}),
            'currency': forms.Select(attrs={ 'class':'form-control'}),
            'paymentterm': forms.Select(attrs={ 'class':'form-control'}),
            'priceterm': forms.Select(attrs={ 'class':'form-control'}),
            'quote_sales': forms.TextInput(attrs={ 'class':'form-control'}),
            'ord_date': forms.DateInput(attrs={ 'class':'form-control'}),
            'effective_date': forms.DateInput(attrs={ 'class':'form-control'}),
            'comment': forms.Textarea(attrs={ 'class':'form-control'}),
        }
