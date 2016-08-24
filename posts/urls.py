
from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name="list" ),
    url(r'^create/$', views.post_create, name="create" ),
    url(r'^(?P<id>\d+)/detail/$', views.post_detail, name="detail" ),
    url(r'^(?P<id>\d+)/detail/edit/$', views.post_update, name="edit" ),
    url(r'^(?P<id>\d+)/detail/delete/$', views.post_delete, name="delete" ),
]
