from django.contrib import admin
from . import models

# Register your models here.


class AttachmentInline(admin.TabularInline):
    model = models.Attachment


class PostAdmin(admin.ModelAdmin):
    list_display = ('istop', 'categories','subject', 'timestemp', 'modify')
    list_display_links = ('istop', 'subject' ,'timestemp', 'modify')
    inlines = [AttachmentInline]


admin.site.register(models.Category)
admin.site.register(models.Post, PostAdmin)
