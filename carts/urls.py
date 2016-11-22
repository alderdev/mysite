from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^itemcount/$', views.ItemCountView.as_view() , name="item_count"),
    url(r'^$', views.CartView.as_view() , name="cart"),

]
