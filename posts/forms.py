from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    subject = forms.CharField( widget=forms.TextInput( attrs={'class':'form-control' , 'size':'30' } ) )
    content = forms.CharField( widget=forms.Textarea( attrs={'class':'form-control', 'size':'30', 'rows':'20'} ) )

    class Meta:
        model = Post
        exclude = ('create_at','modify' )
