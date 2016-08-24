from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    subject = models.CharField(max_length=60)
    content = models.TextField()
    timestemp = models.DateTimeField(auto_now_add=True, auto_now=False)
    modify = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse( "posts:detail", kwargs={"id": self.id} )
