from django.db import models
from django.core.urlresolvers import reverse
from customers.models import Customer

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('quoted:product_list_by_category',args=[self.slug])




class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products')
    family = models.CharField(max_length=30, null=False, blank=False)
    name = models.CharField(max_length=60)
    modelname = models.TextField(blank=True)
    slug = models.SlugField(max_length=200)
    option1 = models.CharField(max_length=60, null=False, blank=False)
    beam_angle = models.CharField(max_length=60, null=False, blank=False)
    cct = models.CharField(max_length=60, null=False, blank=False)
    cri = models.CharField(max_length=60, null=False, blank=False)
    watt = models.CharField(max_length=60, null=False, blank=False)
    lm = models.CharField(max_length=60, null=False, blank=False)
    image = models.ImageField( null=True, blank=True, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField( null=True, blank=True, default=0)
    width_field = models.IntegerField( null=True, blank=True, default=0)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(null=True, blank=True, default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)


    def __str__(self):
        return self.modelname

    def get_absolute_url(self):
        return reverse('quoted:product_detail',args=[self.id, self.slug])


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product,  related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
