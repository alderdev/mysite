from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import WorkOrder
from .forms import WorkOrderCreateForm, WorkOrderUpdateForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.



class WorkOrderList(ListView):
    model = WorkOrder
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query_list = WorkOrder.objects.filter(
                Q(customer__title__icontains=query)|
                Q(product__part_number=query)

            ).distinct()

            return query_list

        return WorkOrder.objects.all()



class WorkOrderDetail(DetailView):
    model = WorkOrder
    form_class = WorkOrderUpdateForm


    def get_object(self):
        # Call the superclass
        object = super(WorkOrderDetail, self).get_object()
        # Record the last accessed date
        object.last_accessed = timezone.now()
        object.save()
        # Return the object
        return object


class WorkOrderCreate(CreateView):
    model = WorkOrder
    form_class = WorkOrderCreateForm
    success_url = reverse_lazy('workorders:list')


class WorkOrderUpdate(UpdateView):
    model = WorkOrder
    form_class = WorkOrderUpdateForm
    success_url = reverse_lazy('workorders:list') #因為不會回到該項資料的Detail, 所以先回到List吧


class WorkOrderDelete(DeleteView):
    model = WorkOrder
    success_url = reverse_lazy('workorders:list')
