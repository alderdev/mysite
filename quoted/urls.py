from django.conf.urls import url
from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^order/$',login_required( views.OrderList.as_view( template_name = 'quoted/order_list.html')), name="order_list" ),
    url(r'^order/(?P<id>\d+)/$', views.order_detail, name="order_detail" ),
    url(r'^order/(?P<pk>\d+)/$', views.OrderDetail.as_view( template_name = 'quoted/order_detail.html'), name="order_detail" ),

    url(r'^order/itemedit/(?P<pk>\d+)/$', views.OrderItemDetail.as_view( template_name = 'quoted/orderitem_detail.html'), name="orderitem_detail" ),


    url(r'^order/(?P<pk>\d+)/update/$', views.OrderUpdate.as_view( template_name = 'quoted/order_updateform.html'), name="order_update" ),
    url(r'^order/(?P<id>\d+)/gen_quote/$', views.gen_quote , name="gen_quote" ),
    url(r'^order/(?P<id>\d+)/gen_pdfv2/$', views.gen_pdfv2 , name="gen_pdfv2" ),
    #url(r'^order/(?P<id>\d+)/print/$', views.order_print , name="order_print" ),
    url(r'^order/(?P<id>\d+)/iteminsert/$', views.order_item_insert ),
    url(r'^order/(?P<id>\d+)/deleteitem/$', views.quote_delete_item ),
    url(r'^insertitem/$', views.order_item_insert ),

    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^$', views.product_list, name='product_list'),

    url(r'^(?P<category_slug>[-\w]+)/$',    views.product_list,    name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',    views.product_detail,    name='product_detail'),
    #url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$',    views.ProductDetail.as_view(),    name='product_detail'),

    #CBV
    #url(r'^$', views.ProductList.as_view( template_name='quoted/product/product_list.html' ), name='product_list'),






]
