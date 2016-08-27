from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    #(r'^$', views.EmployeeList.as_view( template_name = 'employees/employee_list.html'), name="list" ),
    #url(r'^create/$', views.employee_create, name="create" ),
    #url(r'^create/$', views.EmployeeCreate.as_view( template_name = 'employees/employee_form.html' ), name="create" ),
    #url(r'^(?P<pk>[0-9]+)/detail/$', views.EmployeeDetail.as_view( template_name = 'employees/employee_detail.html'), name="detail" ),
    #url(r'^(?P<pk>\d+)/detail/edit/$', views.EmployeeUpdate.as_view( template_name = 'employees/employee_form.html' ), name="edit" ),
    #url(r'^(?P<pk>\d+)/detail/delete/$', views.ProductDelete(), name="delete" ),
    #url(r'^(?P<id>\d+)/detail/edit/$', views.product_update, name="edit" ),
    #url(r'^(?P<id>\d+)/detail/delete/$', views.product_delete, name="delete" ),
]
