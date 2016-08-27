
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from .models import Customer

# Create your views here.
class CustomerList(ListView):
    model = Customer


class CustomerDetail(DetailView):
    model = Customer
