from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import QuoteHead, QuoteDetail,OrderNumberManager
from .forms import QuoteHeadCreateForm, QuoteDetailAddinForm





# Create your views here.
class QuotationList(ListView):
    model = QuoteHead
    paginate_by = 5


class QuotationDetail(DetailView):
    model = QuoteHead
    form_class = QuoteDetailAddinForm



class QuotationCreate(CreateView):
    model = QuoteHead
    form_class = QuoteHeadCreateForm

    def form_valid(self, form):
        #自動取得單據流水號
        form.instance.order_number = QuoteHead.objects.month_sequence()
        form.instance.request_user = self.request.user

        return super(QuotationCreate, self).form_valid(form)



class QuoteDetailCreate( CreateView):
    model = QuoteDetail
    form_class = QuoteDetailAddinForm
    #success_url = '/quotations'

    def form_valid(self, form):
        #自動取得單據流水號
        form.instance.order_number = QuoteHead.objects.month_sequence()
        form.instance.request_user = self.request.user

        return super(QuotationCreate, self).form_valid(form)



def quote_create_line(request):

    form = QuoteDetailAddinForm(request.POST or None )
    #print( form.quotehead.id )
    if form.is_valid():

        instance = form.save(commit=False)
        print(QuoteDetail.objects.current_number())
        instance.save()
        #messages.success(request, "Successfully Create Line")
        #print( instance.quotehead.id )
        return HttpResponseRedirect("../%s" %str(instance.quotehead.id))
        #return HttpResponseRedirect(instance.get_absolute_url())

    return render(request, "quotations/quotation_detail.html", locals())
