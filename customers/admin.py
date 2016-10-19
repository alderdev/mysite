from django.contrib import admin
from . import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('sap_no', 'title', 'contact', 'email','phone','phone_ext',)
    list_per_page = 10

admin.site.register(models.Customer, CustomerAdmin)

# Register your models here.
