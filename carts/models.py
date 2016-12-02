from django.conf import settings
from django.db import models
from quoted.models import Product
from django.core.urlresolvers import reverse

# Create your models here.

class CartItems(models.Model):
    cart = models.ForeignKey( "Cart" )
    item = models.ForeignKey( Product )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity1 = models.PositiveIntegerField(null=True, blank=True)
    price1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity2 = models.PositiveIntegerField(null=True, blank=True)
    price2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity3 = models.PositiveIntegerField(null=True, blank=True)
    price3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.item.name

    def remove(self):
        return "%s?item=%s&delete=True"%( reverse("carts"),self.item.id)



class Cart(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL,null=True, blank=True )
    items = models.ManyToManyField(Product ,through=CartItems)

    def __str__(self):
        return str(self.id)
