from django.db import models
from django.core.urlresolvers import reverse
from smart_selects.db_fields import ChainedForeignKey
from django.utils import timezone
# Create your models here.


class Department(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']


class Job(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']

class Employee(models.Model):
    department = models.ForeignKey(Department)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    english_name = models.CharField(max_length = 60)
    job = models.ForeignKey(Job)
    emp_number = models.CharField(max_length = 6, unique=True)
    contact_ext = models.CharField(max_length=4, blank=True, null=True )
    dutydate = models.DateField( default=timezone.now )
    on_duty = models.BooleanField( default=True )
    image = models.ImageField( null=True, blank=True, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField( null=True, blank=True, default=0)
    width_field = models.IntegerField( null=True, blank=True, default=0)
    description = models.TextField(null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True, auto_now =False) #
    modify = models.DateTimeField(auto_now_add=False, auto_now =True) #

    def __str__(self):
        return "%s %s" %(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse( "employees:detail", kwargs={"pk": self.id} )

    class Meta:
        ordering = ['-emp_number']
