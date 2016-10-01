from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from .models import Order
from customers.models import Customer

class OrderCreateForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset = Customer.objects.all(), widget=forms.TextInput )

    class Meta:
        model = Order
        fields = ['customer', 'email']
        raw_id_fields = ('customer',)
