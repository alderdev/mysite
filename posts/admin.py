from django.contrib import admin
from . import models

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['description', 'slug']
    prepopulated_fields = {'slug': ('description',)}

admin.site.register(models.Category, CategoryAdmin)

class AttachmentInline(admin.TabularInline):
    model = models.Attachment


class PostAdmin(admin.ModelAdmin):
    list_display = ('istop', 'categories','subject', 'timestemp', 'modify')
    list_display_links = ('istop', 'subject' ,'timestemp', 'modify')
    inlines = [AttachmentInline]



admin.site.register(models.Post, PostAdmin)
