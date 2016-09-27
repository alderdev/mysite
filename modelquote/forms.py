from django import forms
from django.utils import timezone
from customers.models import Customer
from quotations.models import Currency
from modelquote.models import ModelQuote
from prod_model.models import ProdModel
from pagedown.widgets import PagedownWidget

class ModelQuoteCreateForm(forms.ModelForm):

    customer = forms.ModelChoiceField( queryset= Customer.objects.all() ,
                                        widget= forms.TextInput( attrs={'class':'form-control' , 'onfocus':'select()' } ) ) #客戶編號

    ord_date = forms.DateField(initial=timezone.now ,
                               widget= forms.DateInput(
                                                        attrs={'class':'form-control' ,
                                                                'size':'30' ,
                                                                'placeholder':'yyyy-MM-dd' ,
                                                                'onfocus':'select()'
                                                                 }
                                                        )
                                 ) #報價日期

    effective_date = forms.DateField(initial=timezone.now ,
                                    widget= forms.DateInput( attrs={'class':'form-control' , 'size':'30' , 'onfocus':'select()', 'placeholder':'yyyy-MM-dd'  } ) ) # 報價單有效日期

    currency = forms.ModelChoiceField( queryset= Currency.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )
    comment = forms.CharField( widget=forms.Textarea( attrs={'class':'form-control', 'size':'30', 'rows':'20'} ), required=False  )

    class Meta:
        model = ModelQuote
        exclude = ( 'create_at','modify','invalid', 'order_number', 'request_user' )
