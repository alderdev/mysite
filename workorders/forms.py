from django import forms
from customers.models import Customer
from products.models import Product
from .models import OrderCategory, ZmmsOption, MaterialCtrlOption, WorkOrder
from pagedown.widgets import PagedownWidget
from django.utils import timezone


class WorkOrderCreateForm(forms.ModelForm):

    recevice_date = forms.DateField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'yyyy-MM-dd'  } ) )
    ships_order = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Ship Order Number' } )   )
    work_order = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Work Order Number'  } ) )
    ord_amount = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Amount'  } ) )
    deliverly = forms.DateField( widget= forms.SelectDateWidget()  )
    reuqest_user = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Reuqest User'  } )  )

    material_duty = forms.CharField( widget=forms.TextInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Material Duty' } ) )
    manage_memo = forms.CharField( widget= PagedownWidget( attrs={'class':'form-control', 'size':'30', 'rows':'20'} )  )

    category = forms.ModelChoiceField( queryset= OrderCategory.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )
    customer = forms.ModelChoiceField( queryset= Customer.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )
    product = forms.ModelChoiceField( queryset= Product.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )

    class Meta:
        model = WorkOrder
        exclude = ('create_at','modify','last_access' ,'estimated_finish', 'zmms', 'material_ctrl', 'material_ready_date')


class WorkOrderUpdateForm(forms.ModelForm):

    recevice_date = forms.DateField( widget= forms.SelectDateWidget() )
    ships_order = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Customer Title'} )  )
    work_order = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Address'} ) )
    ord_amount = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Contact Person'  } ) )
    deliverly = forms.DateField( widget= forms.SelectDateWidget()  )
    material_ready_date = forms.DateField( widget= forms.SelectDateWidget()  )
    estimated_finish = forms.DateField(widget= forms.SelectDateWidget()  )
    reuqest_user = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Email Address'  } ) )

    material_duty = forms.CharField(widget=forms.TextInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Fax Number' } ) )
    manage_memo = forms.CharField( widget= PagedownWidget( attrs={'class':'form-control', 'size':'30', 'rows':'20'} ) )

    category = forms.ModelChoiceField( queryset= OrderCategory.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )
    zmms = forms.ModelChoiceField( queryset= ZmmsOption.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} )  )
    material_ctrl = forms.ModelChoiceField( queryset= MaterialCtrlOption.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} )  )
    customer = forms.ModelChoiceField( queryset= Customer.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )
    product = forms.ModelChoiceField( queryset= Product.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )

    class Meta:
        model = WorkOrder
        exclude = ('create_at','modify' )
