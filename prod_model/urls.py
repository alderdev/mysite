from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    # Class Base View
    url(r'^$', views.ProdModelList.as_view( template_name = 'prod_model/prod_model_list.html' ), name="list" ),
    #url(r'^create/$', views.QuotationCreate.as_view(template_name = 'prod_model/quotation_form.html' ),   name="create" ),
    url(r'^(?P<pk>\d+)/$', views.ProdModelDetail.as_view( template_name = 'prod_model/prod_model_detail.html'), name="detail" ),
    #url(r'^(?P<pk>\d+)/edit/$', views.CustmerUpdate.as_view( template_name = 'prod_model/customer_form.html' ), name="edit" ),
    #url(r'^(?P<pk>\d+)/delete/$', views.CustomerDelete.as_view(), name="delete" ),



    #url(r'^detailadd/$', views.quote_create_line  ),


    #url(r'^detailadd/$', views.QuoteDetailCreate.as_view( template_name = 'quotations/quotation_detail.html'), name="detailadd" ),

]
