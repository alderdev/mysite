from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    # Class Base View
    url(r'^$', views.AuthorList.as_view( template_name = 'exam/author_list.html' ), name="list" ),
    url(r'^create/$', views.AuthorCreate.as_view(template_name = 'exam/author_form.html' ),   name="create" ),
    url(r'^(?P<pk>\d+)/$', views.AuthorDetail.as_view( template_name = 'exam/author_detail.html'), name="detail" ),
    #url(r'^(?P<pk>\d+)/edit/$', views.CustmerUpdate.as_view( template_name = 'customers/customer_form.html' ), name="edit" ),
    #url(r'^(?P<pk>\d+)/delete/$', views.CustomerDelete.as_view(), name="delete" ),


    #url(r'^ajax/(?P<pk>\d+)/$', views.CustomerDetail.as_view( template_name = 'customers/jquery_customer.html'), name="detail" ),


]
