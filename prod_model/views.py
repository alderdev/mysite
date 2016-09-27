from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import ProdModel
from .forms import ProdModelForm



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
