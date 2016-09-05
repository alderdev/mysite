
from django.shortcuts import render
from django.http import HttpResponse
from django import views
from django.contrib import auth
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required



def index(request):
    title="Mysite Home"
    #return HttpResponse("<h1>%s</h1>" %(title))
    return render( request, 'index.html', locals() )



def logout(request):
    auth.logout(request)
    return render( request, 'index.html', locals() )



def login(request):
    auth.logout(request)
    return render( request, 'index.html', locals() )
