
from django.shortcuts import render
from django.http import HttpResponse
from django import views


def index(request):
    title="Mysite Home"
    #return HttpResponse("<h1>%s</h1>" %(title))
    return render( request, 'index.html', locals() )
