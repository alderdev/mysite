from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import ProdModel
#from .forms import QuoteHeadCreateForm, QuoteDetailAddinForm

class ProdModelList(ListView):
    model = ProdModel
    paginate_by = 10


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
