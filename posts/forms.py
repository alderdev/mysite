from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        exclude = ('create_at','modify' )
