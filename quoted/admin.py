from django.contrib import admin
from .models import Category, Product, Order, OrderItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'modelname', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'family', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):

    list_display = [ 'customer','email','paid','created', 'updated']
    raw_id_fields = ['customer']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
