from django.contrib import admin
from . import models




class ContactInline(admin.TabularInline):
    model = models.Contact
    raw_id_fields = ['customer']
    extra = 0


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('sap_no', 'title', 'address','phone','faxno')
    list_display_links = ('sap_no', 'title', 'phone',)
    list_per_page = 10
    search_fields = ['title']

    inlines = [ContactInline]

admin.site.register(models.Customer, CustomerAdmin)
