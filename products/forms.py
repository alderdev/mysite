from django import forms
from .models import Product
from pagedown.widgets import PagedownWidget

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('create_at','modify','height_field', 'width_field' )

        
