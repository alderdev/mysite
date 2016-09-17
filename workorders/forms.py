from django import forms
from customers.models import Customer
from products.models import Product
from .models import OrderCategory, ZmmsOption, MaterialCtrlOption, WorkOrder
from pagedown.widgets import PagedownWidget
from django.utils import timezone


class WorkOrderCreateForm(forms.ModelForm):

    recevice_date = forms.DateField(initial=timezone.now , widget= forms.DateInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'yyyy-MM-dd'  } ) )
    ships_order = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Ship Order Number' } ) , required=False    )
    work_order = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Work Order Number'  } ) )
    ord_amount = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Amount'  } ) )
    #deliverly = forms.DateField( widget= forms.SelectDateWidget()  )
    deliverly = forms.DateField( widget= forms.DateInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'yyyy-MM-dd' } ) )
    request_user = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Request User'  } )  )

    material_duty = forms.CharField( widget=forms.TextInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Material Duty' } ) , required=False )
    manage_memo = forms.CharField( widget=forms.Textarea( attrs={'class':'form-control', 'size':'30', 'rows':'20'} ), required=False  )

    category = forms.ModelChoiceField( queryset= OrderCategory.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )
    customer = forms.ModelChoiceField( queryset= Customer.objects.all() ,
                                        widget= forms.TextInput( attrs={'class':'form-control' } ) )
    product = forms.ModelChoiceField( queryset= Product.objects.all() ,
                                        widget= forms.TextInput( attrs={'class':'form-control'} ) )

    class Meta:
        model = WorkOrder
        exclude = ('create_at','modify','last_access' ,'estimated_finish', 'zmms', 'material_ctrl', 'material_ready_date')


class WorkOrderUpdateForm(forms.ModelForm):

    recevice_date = forms.DateField( widget= forms.DateInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'yyyy-MM-dd' } ) )
    ships_order = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Customer Title'} ), required=False  )
    work_order = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Address'} ) )
    ord_amount = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Contact Person'  } ) )
    deliverly = forms.DateField( widget= forms.DateInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'yyyy-MM-dd' } ) )
    material_ready_date = forms.DateField( widget= forms.DateInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'yyyy-MM-dd' } ) )
    estimated_finish = forms.DateField(widget= forms.DateInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'yyyy-MM-dd' } ) )
    request_user = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Request User'  } ) )

    material_duty = forms.CharField(widget=forms.TextInput( attrs={'class':'form-control', 'size':'30' , 'placeholder':'Material Duty' } ) )
    manage_memo = forms.CharField( widget=forms.Textarea( attrs={'class':'form-control', 'size':'30', 'rows':'20'} ) )

    category = forms.ModelChoiceField( queryset= OrderCategory.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )
    zmms = forms.ModelChoiceField( queryset= ZmmsOption.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} )  )
    material_ctrl = forms.ModelChoiceField( queryset= MaterialCtrlOption.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} )  )
    customer = forms.ModelChoiceField( queryset= Customer.objects.all() ,widget= forms.TextInput( attrs={'class':'form-control'  } ) )
    product = forms.ModelChoiceField( queryset= Product.objects.all() ,widget= forms.TextInput( attrs={'class':'form-control'  } ) )

    class Meta:
        model = WorkOrder
        exclude = ('create_at','modify' )
