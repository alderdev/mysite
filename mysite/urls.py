"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.contrib.auth.views import login, logout

from .views import index, logout
from posts import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', index),
    url(r'^$', views.post_list, name="list" ),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^posts/', include( 'posts.urls', namespace="posts")),
    url(r'^products/', include( 'products.urls', namespace="products")),
    url(r'^employees/', include( 'employees.urls', namespace="employees")),
    url(r'^workorders/', include( 'workorders.urls', namespace="workorders")),
    url(r'^customers/', include( 'customers.urls', namespace="customers")),
    url(r'^quotations/', include( 'quotations.urls', namespace="quotations")),

    url(r'^exam/', include( 'exam.urls', namespace="exam")),
    url(r'^prod_model/', include( 'prod_model.urls', namespace="prod_model")),
    url(r'^cart/', include( 'cart.urls', namespace="cart")),
    url(r'^modelquote/', include( 'modelquote.urls', namespace="modelquote")),
    url(r'^quoted/', include( 'quoted.urls', namespace="quoted")),

    url(r'^chaining/', include('smart_selects.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
