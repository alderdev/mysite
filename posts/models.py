from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Post(models.Model):
    subject = models.CharField(max_length=60)
    content = models.TextField()
    #image = models.ImageField( null=True, blank=True, height_field="height_field", width_field="width_field")
    image = models.URLField( null=True, blank=True)
    height_field = models.IntegerField(default=24)
    width_field = models.IntegerField(default=24)
    timestemp = models.DateTimeField(auto_now_add=True, auto_now=False)
    modify = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse( "posts:detail", kwargs={"id": self.id} )
