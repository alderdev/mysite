from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from .forms import  PostForm
# Create your views here.


def post_list(request):
    title="公告事項"
    object_list = models.Post.objects.all()
    return render(request, "post_list.html", locals())



def post_create(request):
    title="Posts Create"
    form = PostForm(request.POST or None , request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect( instance.get_absolute_url() )


    return render(request, "post_form.html", locals())



def post_detail(request, id):
    title="Posts Detail"
    instance = get_object_or_404(models.Post, id=id)
    return render(request, "post_detail.html", locals())



def post_update(request, id):
    title="Posts Edit"

    instance = get_object_or_404(models.Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect( instance.get_absolute_url() )

    return render(request, "post_form.html", locals())



def post_delete(request, id):
    instance = get_object_or_404(models.Post, id=id)
    instance.delete()

    return redirect("posts:list")
