from django import forms



class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField()
    price = forms.FloatField()
    quantity1 = forms.IntegerField()
    price1 = forms.FloatField()
    quantity2 = forms.IntegerField()
    price2 = forms.FloatField()
    quantity3 = forms.IntegerField()
    price3 = forms.FloatField()

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput
                                )
