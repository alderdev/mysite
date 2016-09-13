from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q

from .models import QuoteHead

# Create your views here.
class QuotationList(ListView):
    model = QuoteHead
    paginate_by = 10


class QuotationDetail(DetailView):
    model = QuoteHead
