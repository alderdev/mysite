
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from .models import Customer
from . import forms

# Create your views here.
class CustomerList(ListView):
    model = Customer


class CustomerDetail(DetailView):
    model = Customer


class CustomerCreateView(CreateView):

    form_class = forms.CustomerCreateForm
    success_url = '/customers'



class CustmerUpdate(UpdateView):
    model = Customer
    form_class = forms.CustomerUpdateForm
    success_url = reverse_lazy('customers:list') #因為不會回到該項資料的Detail, 所以先回到List吧



class CustomerDelete(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers:list')
