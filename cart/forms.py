from django import forms



class CartAddProductForm(forms.Form):
    price = forms.FloatField()

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput
                                )
