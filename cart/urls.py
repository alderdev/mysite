from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    # Class Base View
    url(r'^$', views.cart_detail, name="cart_detail"),
    #url(r'^create/$', views.QuotationCreate.as_view(template_name = 'prod_model/quotation_form.html' ),   name="create" ),

    url(r'^(?P<product_id>\d+)/add/$', views.cart_add , name="cart_add"),
    url(r'^remove/(?P<product_id>\d+)/$',views.cart_remove,name='cart_remove'),


    #url(r'^add/(?P<pk>\d+)/$', views.cart_add , name="cart_add"),
    #url(r'^(?P<pk>\d+)/edit/$', views.CustmerUpdate.as_view( template_name = 'prod_model/customer_form.html' ), name="edit" ),
    #url(r'^(?P<pk>\d+)/delete/$', views.CustomerDelete.as_view(), name="delete" ),



    #url(r'^detailadd/$', views.quote_create_line  ),


    #url(r'^detailadd/$', views.QuoteDetailCreate.as_view( template_name = 'quotations/quotation_detail.html'), name="detailadd" ),

]
