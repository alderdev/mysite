from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from smart_selects.db_fields import ChainedForeignKey
from .models import ModelQuote, QuoteLine
from .forms import ModelQuoteCreateForm, QuoteLineAddinForm

# Create your views here.
class ModelQuoteList( ListView):
    model = ModelQuote
    paginate_by = 5


class ModelQuoteCreate( CreateView ):
    model =ModelQuote
    form_class = ModelQuoteCreateForm

    def form_valid(self, form):
        #自動取得單據流水號
        form.instance.order_number = ModelQuote.objects.short_month_sequence()
        form.instance.request_user = self.request.user

        return super( ModelQuoteCreate, self).form_valid(form)


class ModelQuoteDetail( DetailView ):
    model = ModelQuote



class ModelQuoteUpdate( UpdateView ):
    model = ModelQuote
    form_class = ModelQuoteCreateForm



def quoteline_create(request):
    form = QuoteLineAddinForm(request.POST or None )

    if form.is_valid():

        instance = form.save(commit=False)
        instance.line_no = QuoteLine.objects.current_number(instance.quotehead_id)
        instance.save()
        return HttpResponseRedirect("../%s" %str(instance.quotehead.id))

    return render(request, "modelquote/modelquote_detail.html", locals())
