
from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.ProductList.as_view( template_name = 'products/product_list.html'), name="list" ),
    url(r'^create/$', views.ProductCreate.as_view( template_name = 'products/product_form.html' ), name="create" ),
    url(r'^(?P<pk>[0-9]+)/$', views.ProductDetail.as_view( template_name = 'products/product_detail.html'), name="detail" ),
    #url(r'^(?P<pk>\d+)/detail/edit/$', views.ProductUpdate.as_view( template_name = 'products/product_form.html' ), name="edit" ),
    #url(r'^(?P<pk>\d+)/detail/delete/$', views.ProductDelete(), name="delete" ),
    url(r'^(?P<id>\d+)/edit/$', views.product_update, name="edit" ),
    url(r'^(?P<id>\d+)/delete/$', views.product_delete, name="delete" ),



    url(r'^ajax/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view( template_name = 'products/jquery_product.html'), name="detail" ),

]
