from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)



class Category(models.Model):
    description = models.CharField(max_length=30, blank=False, null=False )
    slug = models.SlugField(max_length=30,unique=True)

    class Meta:
        ordering = ('description',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.description


    def get_absolute_url(self):
        return reverse('posts:post_list_by_category', args=[ self.slug ])



class Post(models.Model):
    categories = models.ForeignKey(Category, default=1)
    subject = models.CharField(max_length=60)
    content = models.TextField()

    #image = models.ImageField( null=True, blank=True, height_field="height_field", width_field="width_field")
    #height_field = models.IntegerField(default=24)
    #width_field = models.IntegerField(default=24)

    timestemp = models.DateTimeField(auto_now_add=True, auto_now=False)
    modify = models.DateTimeField(auto_now_add=False, auto_now=True)
    available = models.BooleanField(default=True)
    istop = models.BooleanField(default=False)

    class Meta:
        ordering = [ '-istop', '-modify','id' ]

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse( "posts:detail", kwargs={"pk": self.pk} )



class Attachment(models.Model):
    post = models.ForeignKey( Post, blank=True, null=True )
    filename = models.FileField(blank=True, null=True)
    remark = models.CharField(max_length=60, blank=True, null=True )
    timestemp = models.DateTimeField(auto_now_add=True, auto_now=False)
    modify = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.filename
