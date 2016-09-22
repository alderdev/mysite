from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class ProdModel(models.Model):
    family = models.CharField(max_length=30, null=False, blank=False)
    prodname = models.CharField(max_length=60, null=False, blank=False)
    modelname = models.CharField(max_length=60, null=False, blank=False)
    option1 = models.CharField(max_length=60, null=False, blank=False)
    beam_angle = models.CharField(max_length=60, null=False, blank=False)
    cct = models.CharField(max_length=60, null=False, blank=False)
    cri = models.CharField(max_length=60, null=False, blank=False)
    watt = models.CharField(max_length=60, null=False, blank=False)
    lm = models.CharField(max_length=60, null=False, blank=False)
    image = models.ImageField( null=True, blank=True, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField( null=True, blank=True, default=0)
    width_field = models.IntegerField( null=True, blank=True, default=0)
    is_active = models.BooleanField(default=True) #是否還在生產


    def __str__(self):
        return self.modelname


    def get_absolute_url(self):
        return reverse( "prod_model:detail", kwargs={"pk": self.id} )
