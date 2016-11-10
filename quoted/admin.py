from django.contrib import admin
from .models import Category, Product, Order, OrderItem, PaymentTerm, PriceTerm, DimmingOption, ProductPrice



class PriceTermAdmin(admin.ModelAdmin):
    list_display = ['description']

admin.site.register(PriceTerm, PriceTermAdmin)



class PaymentTermAdmin(admin.ModelAdmin):
    list_display = ['description']


class DimmingOptionAdmin(admin.ModelAdmin):
    list_display = ['description']

admin.site.register(DimmingOption, DimmingOptionAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)




class PriceInline(admin.TabularInline):
    model = ProductPrice
    raw_id_fields = ['product','currency']



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'modelname', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'category', 'family', 'watt']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PriceInline]

admin.site.register(Product, ProductAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']



class OrderAdmin(admin.ModelAdmin):

    list_display = [ 'is_valid','order_number','customer','email','quote_sales','ord_date', 'effective_date']
    list_display_links = ['order_number','customer','email']
    raw_id_fields = ['customer']
    list_filter = ['is_valid', 'quote_sales']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
