from django import forms
from .models import People


class PeopleForm(forms.ModelForm):

    class Meta:
        model = People
        exclude = ('height_field', 'width_field', 'create_at', 'modify' )
