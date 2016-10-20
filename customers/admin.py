from django.contrib import admin
from . import models




class ContactInline(admin.TabularInline):
    model = models.Contact
    raw_id_fields = ['customer']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('sap_no', 'title', 'phone',)
    list_per_page = 10
    inlines = [ContactInline]

admin.site.register(models.Customer, CustomerAdmin)
