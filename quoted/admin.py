from django.contrib import admin
from .models import Category, Product, Order, OrderItem, PaymentTerm, PriceTerm



class PriceTermAdmin(admin.ModelAdmin):
    list_display = ['description']

admin.site.register(PriceTerm, PriceTermAdmin)



class PaymentTermAdmin(admin.ModelAdmin):
    list_display = ['description']

admin.site.register(PaymentTerm, PaymentTermAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'modelname', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'category', 'family', 'watt']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']



class OrderAdmin(admin.ModelAdmin):

    list_display = [ 'customer','email','created', 'updated','paid']
    raw_id_fields = ['customer']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
