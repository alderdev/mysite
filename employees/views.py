from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from smart_selects.db_fields import ChainedForeignKey

from . import models
from .forms import EmployeeForm




class EmployeeList(ListView):
    model = models.Employee
    #context_object_name = 'my_favorite_publishers'



class EmployeeDetail(DetailView):
    model = models.Employee
    
    def get_context_data(self, **kwargs):
        context = super( EmployeeDetail, self).get_context_data(**kwargs)
        context['Employee_list'] = models.Employee.objects.all()
        return context



def employee_create(request):
    title="Posts Create"
    form = EmployeeForm(request.POST or None , request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect( instance.get_absolute_url() )


    return render(request, "employees/employee_form.html", locals())





class EmployeeCreate(CreateView):

    model = models.Employee
    fields = ['department', 'first_name', 'last_name',  'english_name', 'job', 'emp_number','contact_ext','dutydate'
    ,'on_duty', 'image', 'description'
    ]
    success_url = '/employees'




class EmployeeUpdate(UpdateView):
    model = models.Employee
    fields = ['department', 'first_name', 'last_name',  'english_name', 'job', 'emp_number','contact_ext','dutydate'
    ,'on_duty', 'image', 'description'
    ]
    success_url = reverse_lazy('employees:list') #因為不會回到該項資料的Detail, 所以先回到List吧



class EmployeeDelete(DeleteView):
    model = models.Employee
    #success_url = '/products'
    success_url = reverse_lazy('employees:list')




def employee_update(request, id):

    instance = get_object_or_404(models.Employee, id=id)
    form = EmployeeForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect( instance.get_absolute_url() )

    return render(request, "employees/Employee_form.html", locals())




def employee_delete(request, id):
    instance = get_object_or_404(models.Employee, id=id)
    instance.delete()

    return redirect("employees:list")
