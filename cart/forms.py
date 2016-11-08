from django import forms



class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(widget= forms.TextInput( attrs={'class':'form-control', 'size':4 , 'onfocus':'select()'}))
    price = forms.FloatField()
    quantity1 = forms.IntegerField(required=False,widget= forms.TextInput( attrs={'class':'form-control', 'size':4 , 'onfocus':'select()' } ))
    price1 = forms.FloatField(required=False)
    quantity2 = forms.IntegerField(required=False,widget= forms.TextInput( attrs={'class':'form-control', 'size':4 , 'onfocus':'select()' } ))
    price2 = forms.FloatField(required=False)
    quantity3 = forms.IntegerField(required=False,widget= forms.TextInput( attrs={'class':'form-control', 'size':4 , 'onfocus':'select()' } ))
    price3 = forms.FloatField(required=False)

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput
                                )
