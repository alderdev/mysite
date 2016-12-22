from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from . import models
from django.db.models import Q
from .forms import  PostForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.


class PostList(ListView):
    model = models.Post
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')

        if query:
            query_list = models.Post.objects.filter(
                Q(subject__icontains=query)|
                Q(content__icontains=query)
            ).distinct()
            return query_list

        return models.Post.objects.all()

    def get_context_data(self, *args, **kwargs):

        context = super( PostList, self).get_context_data(*args, **kwargs )
        context['categories'] = models.Category.objects.all()
        #print(context)
        return context

class PostDetail(DetailView):
    model = models.Post


class PostCreate(CreateView):
    model = models.Post
    form_class = PostForm


class PostUpdate(UpdateView):
    model = models.Post
    form_class = PostForm



@login_required
def post_list(request):
    title="公告事項"
    object_list = models.Post.objects.all()
    return render(request, "posts/post_list.html", locals())



@login_required
def posts_list(request, category_slug=None):

    category = None
    categories = models.Category.objects.all()
    object_list = models.Post.objects.filter(available=True)


    if category_slug:
        category = get_object_or_404(models.Category, slug=category_slug)
        object_list = object_list.filter(categories_id=category.id)


    return render(request,'posts/post_list.html',locals() )




@login_required
def post_create(request):
    title="Posts Create"
    form = PostForm(request.POST or None , request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        mailsubject= instance.subject #'Django Send Mail Test'
        mailmessage = instance.content #'Mail Message Content '
        from_email = 'web.service@alder.com.tw'
        to_mail = [ request.user.email ]

        send_mail(mailsubject, mailmessage, from_email, to_mail, fail_silently=False)

        return HttpResponseRedirect( instance.get_absolute_url() )


    return render(request, "posts/post_form.html", locals())


@login_required
def post_detail(request, id):
    title="Posts Detail"
    instance = get_object_or_404(models.Post, id=id)
    return render(request, "posts/post_detail.html", locals())


def post_update(request, id):
    title="Posts Edit"

    instance = get_object_or_404(models.Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect( instance.get_absolute_url() )

    return render(request, "posts/post_form.html", locals())


@login_required
def post_delete(request, id):
    instance = get_object_or_404(models.Post, id=id)
    instance.delete()

    return redirect("posts:list")
