from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',    views.product_list,    name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',    views.product_detail,    name='product_detail'),


]
