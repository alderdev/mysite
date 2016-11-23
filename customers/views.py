
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from .models import Customer
from . import forms
from django.db import transaction

# Create your views here.
class CustomerList(ListView):
    model = Customer
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query_list = Customer.objects.filter(
                Q(title__icontains=query) or Q(sap_no__icontains=query)
            ).distinct()
            return query_list

        return Customer.objects.all()



class CustomerDetail(DetailView):
    model = Customer




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

class CustomerCreateView( AjaxableResponseMixin,CreateView):
    model = Customer
    form_class = forms.CustomerCreateForm
    #success_url = '/customers'
    def get_context_data(self, **kwargs):
        data = super(CustomerCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contacts'] = forms.ContactFormset(self.request.POST)
        else:
            data['contacts'] = forms.ContactFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        contacts = context['contacts']
        self.object = form.save()
        if contacts.is_valid():
            contacts.instance = self.object
            contacts.save()

        return super(CustomerCreateView, self).form_valid(form)




class CustmerUpdate(UpdateView):
    model = Customer
    form_class = forms.CustomerUpdateForm
    #success_url = reverse_lazy('customers:list') #因為不會回到該項資料的Detail, 所以先回到List吧



class CustomerDelete(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers:list')
