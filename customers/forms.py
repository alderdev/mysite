from django import forms
from .models import Customer, Contact
from pagedown.widgets import PagedownWidget

from django.forms.models import modelformset_factory


class CustomerContactForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ('customer',)

CustomerContactFormSet = modelformset_factory(Contact, form=CustomerContactForm,extra=1)

class CustomerSearchForm(forms.ModelForm):
    title = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Customer Title'  } ) )

    class Meta:
        model = Customer
        exclude = ('create_at','modify','invalid' )


class CustomerCreateForm(forms.ModelForm):

    sap_no = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'SAP Customer Number'  } ) )
    title = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Customer Title'  } ) )
    address = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Address'  } ), required=False )
    #contact = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Contact Person'  } ) )
    phone = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Phone Number'  } ), required=False  )
    #phone_ext = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Contact Person Phone Ext '  } ), required=False )
    faxno = forms.CharField(widget=forms.TextInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Fax Number' } ), required=False )
    #email = forms.EmailField( widget= forms.EmailInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Email Address'  } ) , required=False )

    class Meta:
        model = Customer
        #fields = ( 'sap_no', 'title', 'address')
        exclude = ('create_at','modify','invalid' )


class CustomerUpdateForm(forms.ModelForm):

    sap_no = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'SAP Customer Number'  } ) )
    title = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Customer Title'  } ) )
    address = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Address'  } ) )
    contact = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Contact Person'  } ) )
    phone = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Phone Number'  } )  )
    phone_ext = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Contact Person Phone Ext '  } ), required=False )
    faxno = forms.CharField(widget=forms.TextInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Fax Number' } ), required=False )
    email = forms.EmailField( widget= forms.EmailInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Email Address'  } ) , required=False )


    class Meta:
        model = Customer
        exclude = ('create_at','modify' )
