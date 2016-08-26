from django import forms
from .models import Product
from pagedown.widgets import PagedownWidget

class ProductForm(forms.ModelForm):
    part_number = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Part Number'  } ) )



    description = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Description'  } ) )
    specification = forms.CharField( widget= PagedownWidget( attrs={'class':'form-control', 'size':'30', 'rows':'20' , 'placeholder':'Specification' } ) )



    class Meta:
        model = Product
        exclude = ('create_at','modify','height_field', 'width_field' )
