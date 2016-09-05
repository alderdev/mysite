from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy

from . import models
from .forms import ProductForm




class ProductList(ListView):
    model = models.Product
    #context_object_name = 'my_favorite_publishers'



class ProductDetail(DetailView):
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['product_list'] = models.Product.objects.all()
        return context


class ProductCreate(CreateView):
    title = "Create New Product"
    model = models.Product
    form_class = ProductForm
    #fields = ['part_number', 'description', 'specification', 'image',  'category', 'cycle_status']
    success_url = '/products'



class ProductUpdate(UpdateView):
    model = models.Product
    fields = ['part_number', 'description', 'specification', 'image', 'category', 'cycle_status']

    success_url = reverse_lazy('products:list') #因為不會回到該項資料的Detail, 所以先回到List吧



class ProductDelete(DeleteView):
    model = models.Product
    #success_url = '/products'
    success_url = reverse_lazy('products:list')




def product_update(request, id):

    instance = get_object_or_404(models.Product, id=id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect( instance.get_absolute_url() )

    return render(request, "products/product_form.html", locals())




def product_delete(request, id):
    instance = get_object_or_404(models.Product, id=id)
    instance.delete()

    return redirect("products:list")
