from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q

from .models import QuoteHead, QuoteDetail,OrderNumberManager
from .forms import QuoteHeadCreateForm, QuoteDetailAddinForm


from django.http import JsonResponse


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response







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



class QuoteDetailCreate(AjaxableResponseMixin, CreateView):
    model = QuoteDetail
    form_class = QuoteDetailAddinForm
    success_url = '/quotations'
