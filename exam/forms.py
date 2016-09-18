from django import forms
from .models import Author, Book
from django.forms.models import inlineformset_factory


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']

    #BookFormSet = inlineformset_factory(Author, Book, fields=('title',))

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']
