from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Category(models.Model):
    description = models.CharField(max_length=36, null=False, blank=False)
    invalid = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class CycleStatus(models.Model):
    description = models.CharField(max_length=36, null=False, blank=False)
    invalid = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Product(models.Model):

    part_number = models.CharField(max_length=20,null=False, blank=False, unique=True) #SAP料號
    description = models.CharField(max_length=100, null=True, blank=True)
    specification = models.TextField(null=True, blank=True)
    image = models.ImageField( null=True, blank=True, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField( null=True, blank=True, default=0)
    width_field = models.IntegerField( null=True, blank=True, default=0)
    category = models.ForeignKey(Category) #料品分類
    cycle_status = models.ForeignKey(CycleStatus) # 料品狀態

    create_at = models.DateTimeField(auto_now_add=True, auto_now =False) #
    modify = models.DateTimeField(auto_now_add=False, auto_now =True) #

    def __str__(self):
        return self.description


    def get_absolute_url(self):
        return reverse( "products:detail", kwargs={"pk": self.id} )
