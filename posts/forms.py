from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
    subject = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'Subject'  } ) )
    content = forms.CharField( widget=forms.Textarea( attrs={'class':'form-control', 'size':'30', 'rows':'25'} ) )
    #content = forms.CharField( widget= PagedownWidget( attrs={'class':'form-control', 'size':'30', 'rows':'20'} ) )

    class Meta:
        model = Post
        exclude = ('create_at','modify' )
