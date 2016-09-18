from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q

from exam.models import Author, Book
from .forms import AuthorForm
# Create your views here.

class AuthorList(ListView):
    model = Author

class AuthorCreate(CreateView):
    model =Author
    form_class = AuthorForm
    success_url = '/exam'

class AuthorDetail(DetailView):
    model = Author
