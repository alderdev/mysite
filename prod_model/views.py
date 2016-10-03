from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import ProdModel
from .forms import ProdModelForm
from cart.forms import CartAddProductForm


class ProdModelList(ListView):
    model = ProdModel
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query_list = ProdModel.objects.filter(
                Q(prodname__icontains=query)|
                Q(modelname__icontains=query)|
                Q(family=query)
            ).distinct()

            return query_list
        return ProdModel.objects.all()


class ProdModelDetail(DetailView):
    model = ProdModel



class ProdModelCreate( CreateView ):
    model = ProdModel
    form_class = ProdModelForm


class ProdModelUpdate( UpdateView ):
    model = ProdModel
    form_class = ProdModelForm


class ProdModelDelete( DeleteView ):
    model = ProdModel
    success_url = reverse_lazy('prod_model:list')
