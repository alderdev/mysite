from django import forms
from .models import ProdModel
from pagedown.widgets import PagedownWidget

class ProdModelForm(forms.ModelForm):
    family = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Part Number'  } ) )
    prodname = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Description'  } ) )
    option1 = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Part Number'  } ) )
    beam_angle = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Description'  } ) )
    cct = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Part Number'  } ) )
    cri = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Description'  } ) )
    watt = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Part Number'  } ) )
    lm = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Description'  } ) )
    modelname = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Description'  } ) )

    class Meta:
        model = ProdModel
        exclude = ('create_at','modify','height_field', 'width_field', 'is_active' )
