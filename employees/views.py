from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy

from . import models
from .forms import PeopleForm




class EmployeeList(ListView):
    model = models.People
    #context_object_name = 'my_favorite_publishers'



class EmployeeDetail(DetailView):
    model = models.People

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetail, self).get_context_data(**kwargs)
        context['employee_list'] = models.People.objects.all()
        return context


class EmployeeCreate(CreateView):

    model = models.People
    fields = ['department', 'smallpart', 'first_name', 'last_name',  'english_name', 'job', 'emp_number','contact_ext','dutydate'
    ,'on_duty', 'image', 'description'
    ]
    success_url = '/employees'




class EmployeeUpdate(UpdateView):
    model = models.People
    fields = ['department', 'smallpart', 'first_name', 'last_name',  'english_name', 'job', 'emp_number','contact_ext','dutydate'
    ,'on_duty', 'image', 'description'
    ]
    success_url = reverse_lazy('employees:list') #因為不會回到該項資料的Detail, 所以先回到List吧



class EmployeeDelete(DeleteView):
    model = models.People
    #success_url = '/products'
    success_url = reverse_lazy('employees:list')




def employee_update(request, id):

    instance = get_object_or_404(models.People, id=id)
    form = PeopleForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect( instance.get_absolute_url() )

    return render(request, "employees/people_form.html", locals())




def employee_delete(request, id):
    instance = get_object_or_404(models.People, id=id)
    instance.delete()

    return redirect("employees:list")
