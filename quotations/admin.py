from django.contrib import admin
from . import models

# Register your models here.

class QuoteDetailInline(admin.TabularInline):
    model = models.QuoteDetail


class QuoteAdmin(admin.ModelAdmin):
    inlines = [QuoteDetailInline,]

admin.site.register(models.Currency)
admin.site.register(models.QuoteHead, QuoteAdmin)
