from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Department)
admin.site.register(models.Job)
admin.site.register(models.Employee)
