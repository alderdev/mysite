from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    # Class Base View
    url(r'^$',  login_required( views.WorkOrderList.as_view( template_name = 'workorders/workorder_list.html' ) ), name="list" ),
    url(r'^create/$', views.WorkOrderCreate.as_view(template_name = 'workorders/workorder_form.html' ),   name="create" ),
    url(r'^(?P<pk>\d+)/$', views.WorkOrderDetail.as_view( template_name = 'workorders/workorder_detail.html'), name="detail" ),
    url(r'^(?P<pk>\d+)/edit/$', views.WorkOrderUpdate.as_view( template_name = 'workorders/workorder_form.html' ), name="edit" ),
    url(r'^(?P<pk>\d+)/delete/$', views.WorkOrderDelete.as_view(), name="delete" ),

]
