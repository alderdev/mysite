from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q

from .models import QuoteHead, QuoteDetail,OrderNumberManager
from .forms import QuoteHeadCreateForm

# Create your views here.
class QuotationList(ListView):
    model = QuoteHead
    paginate_by = 5


class QuotationDetail(DetailView):
    model = QuoteHead



class QuotationCreate(CreateView):
    model = QuoteHead
    form_class = QuoteHeadCreateForm

    def form_valid(self, form):
        #自動取得單據流水號
        form.instance.order_number = QuoteHead.objects.month_sequence()
        form.instance.request_user = self.request.user

        return super(QuotationCreate, self).form_valid(form)



class QuoteDetailCreate(CreateView):
    model = QuoteDetail
    success_url = '/products'
