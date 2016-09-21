from django.contrib import admin
from . import models

# Register your models here.

class QuoteDetailInline(admin.TabularInline):
    model = models.QuoteDetail



class QuoteAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'ord_date', 'request_user', 'customer','effective_date','currency',)
    list_per_page = 5
    search_fields = ['request_user']
    list_filter =  ('request_user',)
    inlines = [QuoteDetailInline,]

admin.site.register(models.Currency)
admin.site.register(models.QuoteHead, QuoteAdmin)
