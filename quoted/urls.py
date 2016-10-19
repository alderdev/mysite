from django.conf.urls import url
from . import views

urlpatterns = [


    url(r'^order/$', views.OrderList.as_view( template_name = 'quoted/order_list.html'), name="order_list" ),


    url(r'^order/(?P<id>\d+)/$', views.order_detail, name="order_detail" ),
    url(r'^order/(?P<pk>\d+)/$', views.OrderDetail.as_view( template_name = 'quoted/order_detail.html'), name="order_detail" ),

    #url(r'^order/(?P<pk>\d+)/print/$', views.OrderDetail.as_view( template_name = 'quoted/order_print.html'), name="order_print" ),
    url(r'^order/(?P<id>\d+)/print/$', views.order_print , name="order_print" ),
    url(r'^order/(?P<id>\d+)/iteminsert/$', views.order_item_insert ),
    url(r'^order/(?P<id>\d+)/deleteitem/$', views.quote_delete_item ),
    url(r'^insertitem/$', views.order_item_insert ),

    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',    views.product_list,    name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',    views.product_detail,    name='product_detail'),





]
