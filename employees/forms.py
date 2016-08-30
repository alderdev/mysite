from django import forms
from .models import Employee, Job, Department
from smart_selects.db_fields import ChainedForeignKey
from pagedown.widgets import PagedownWidget


class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'First Name'  } ) )
    last_name = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Last Name'  } ) )
    english_name = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'English Name'  } ) )
    description = forms.CharField( widget= PagedownWidget( attrs={'class':'form-control', 'size':'30', 'rows':'20'} ) )
    department = forms.ModelChoiceField( queryset= Department.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )
    job = forms.ModelChoiceField( queryset= Job.objects.all() ,widget= forms.Select( attrs={'class':'form-control'} ) )
    emp_number = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Employee Number'  } ) )
    contact_ext = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Phone Ext'  } ) )
    dutydate = forms.DateField( widget= forms.DateInput( attrs={'class':'form-control' , 'placeholder':'yyyy-MM-dd'   } ) )

    class Meta:
        model = Employee
        exclude = ('height_field', 'width_field', 'create_at', 'modify', 'on_duty' )
