from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    # Class Base View
    url(r'^$', views.QuotationList.as_view( template_name = 'quotations/quotation_list.html' ), name="list" ),
    #url(r'^create/$', views.CustomerCreateView.as_view(template_name = 'customers/customer_form.html' ),   name="create" ),
    url(r'^(?P<pk>\d+)/$', views.QuotationDetail.as_view( template_name = 'quotations/quotation_detail.html'), name="detail" ),
    #url(r'^(?P<pk>\d+)/edit/$', views.CustmerUpdate.as_view( template_name = 'customers/customer_form.html' ), name="edit" ),
    #url(r'^(?P<pk>\d+)/delete/$', views.CustomerDelete.as_view(), name="delete" ),

]
