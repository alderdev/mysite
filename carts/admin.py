from django.contrib import admin
from .models import Cart, CartItems

# Register your models here.
class CartItemsInline(admin.TabularInline):
    model = CartItems
    raw_id_fields = ['item']

class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemsInline
    ]
    class Meta:
        model = Cart
        raw_id_fields = ['user']


admin.site.register(Cart, CartAdmin)
