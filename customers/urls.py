from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    # Class Base View
    url(r'^$', views.CustomerList.as_view( template_name = 'customers/customer_list.html' ), name="list" ),

    # ModelForm Factory  Contact
    url(r'^(?P<pk>\d+)/contact/$', views.ContactList.as_view( template_name = 'customers/contact_list.html' ), name="customer_contact" ),


    url(r'^create/$', views.CustomerCreateView.as_view(template_name = 'customers/customer_form.html' ),   name="create" ),
    url(r'^(?P<pk>\d+)/$', views.CustomerDetail.as_view( template_name = 'customers/customer_detail.html'), name="detail" ),
    url(r'^(?P<pk>\d+)/edit/$', views.CustmerUpdate.as_view( template_name = 'customers/customer_form.html' ), name="edit" ),
    url(r'^(?P<pk>\d+)/delete/$', views.CustomerDelete.as_view(), name="delete" ),


    url(r'^ajax/(?P<pk>\w+)/$', views.CustomerDetail.as_view( template_name = 'customers/jquery_customer.html'), name="ajax_detail" ),

    # Function Base View
    #url(r'^create/$', views.employee_create, name="create" ),
    #url(r'^(?P<id>\d+)/detail/edit/$', views.product_update, name="edit" ),
    #url(r'^(?P<id>\d+)/detail/delete/$', views.product_delete, name="delete" ),
]
