from django import forms



class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField()
    price = forms.FloatField()
    quantity1 = forms.IntegerField(required=False)
    price1 = forms.FloatField(required=False)
    quantity2 = forms.IntegerField(required=False)
    price2 = forms.FloatField(required=False)
    quantity3 = forms.IntegerField(required=False)
    price3 = forms.FloatField(required=False)

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput
                                )
