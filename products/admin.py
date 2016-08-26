from django.contrib import admin


from . import models
from .forms import ProductForm
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm()



admin.site.register(models.Category)
admin.site.register(models.CycleStatus)
admin.site.register(models.Product)
