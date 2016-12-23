from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from customers.models import Customer, Contact
#from quotations.models import Currency
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import User


#幣別
class Currency(models.Model):
    code = models.CharField(primary_key=True, max_length=3, )
    description = models.CharField(max_length=36, null=False, blank=False)

    def __str__(self):
        return self.code


class PaymentTerm(models.Model):
    description = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.description


class PriceTerm(models.Model):
    description = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.description


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
        return reverse('quoted:product_list_by_category',args=[ self.slug ] )



class DimmingOption(models.Model):
    description = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.description



class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products')
    family = models.CharField(max_length=30, null=False, blank=False)
    name = models.CharField(max_length=60)
    modelname = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=200)
    option1 = models.CharField(max_length=60, null=False, blank=False)
    beam_angle = models.CharField(max_length=60, null=False, blank=False)
    cct = models.CharField("CCT",max_length=60, null=False, blank=False)
    cri = models.CharField("CRI",max_length=60, null=False, blank=False)
    watt = models.CharField(max_length=60, null=False, blank=False)
    dimming = models.ForeignKey(DimmingOption,default= 1)
    lm = models.CharField(max_length=60, null=False, blank=False)
    image = models.ImageField( null=True, blank=True, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField( null=True, blank=True, default=0)
    width_field = models.IntegerField( null=True, blank=True, default=0)

    #price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #stock = models.PositiveIntegerField(null=True, blank=True, default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('category','watt','name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.modelname

    def get_absolute_url(self):
        return reverse('quoted:product_detail',args=[self.id, self.slug])



class ProductPrice(models.Model):
    product = models.ForeignKey(Product)
    currency = models.ForeignKey(Currency)
    std_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_sell =  models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = (("product","currency"),)
        ordering = ["-currency"]

    def __str__(self):
        return "%s: %d" %(self.currency, self.std_price)





#自訂單據號碼
class OrderNumberManager(models.Manager):

    #短的月份序號如：16080001
    def short_month_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(created__contains = order_date[:7] ).count()+1
        order_number = nextNumber + int(order_date[2:7].replace('-',''))*10000
        return order_number
    #月份序號如：2016080001
    def month_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(created__contains = order_date[:7] ).count()+1
        order_number = nextNumber + int(order_date[:7].replace('-',''))*10000
        return order_number
    #月份序號如：2016080001
    def day_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(created__contains = order_date ).count()+1
        order_number = nextNumber + int(order_date.replace('-',''))*10000
        return order_number
    #短的日序號如：1608310001
    def short_day_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(created__contains = order_date ).count()+1
        order_number = nextNumber + int(order_date.replace('-','')[2:])*10000
        return order_number



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contact = ChainedForeignKey( Contact,
                        limit_choices_to={'invalid': False},
                        chained_field="customer",
                        chained_model_field="customer",
                        show_all = False,
                        auto_choose= True
                    )
    email = models.EmailField(null=True, blank=True)
    paymentterm = models.ForeignKey(PaymentTerm,null=False, blank=False)
    priceterm = models.ForeignKey(PriceTerm,null=False, blank=False)
    quote_sales = models.CharField(max_length=60, null=True, blank=True) # 取消此欄位, 以quote_user取代
    quote_user = models.ForeignKey( User, null=True, blank=True )
    ord_date = models.DateField(default=timezone.now) #報價日期
    effective_date = models.DateField( default=timezone.now ) # 報價單有效日期
    currency = models.ForeignKey( Currency,  null=False, blank=False )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    order_number = models.CharField(max_length=12, null=True, blank=True, unique=True) #報價單號
    comment = models.TextField(null=True, blank=True)
    objects = OrderNumberManager()
    is_valid = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


    def get_absolute_url(self):
        return reverse('quoted:order_detail', kwargs={"pk": self.id} )



class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product,  related_name='order_items')
    is_special = models.BooleanField('Customized Product',default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    price1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity1 = models.PositiveIntegerField( null=True, blank=True)
    price2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity2 = models.PositiveIntegerField( null=True, blank=True)
    price3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity3 = models.PositiveIntegerField( null=True, blank=True)
    line_remark = models.CharField("Remark",max_length=60, null=True, blank=True)
    #為了解決大量客製化產品的問題,所以將產品規格的欄位一起複製過來, 以便有需求時可以直接編輯
    orderitem_name = models.CharField("product name",max_length=60, null=False, blank=False)
    orderitem_modelname = models.CharField("Model Name",max_length=60, null=False, blank=False)
    orderitem_option1 = models.CharField("Option",max_length=60, null=False, blank=False)#
    orderitem_beam_angle = models.CharField("Beam angle",max_length=60, null=False, blank=False)#
    orderitem_cct = models.CharField("CCT",max_length=60, null=False, blank=False)#
    orderitem_cri = models.CharField("CRI",max_length=60, null=False, blank=False)#
    orderitem_watt = models.CharField("WATT",max_length=60, null=False, blank=False)#
    orderitem_dimming = models.ForeignKey( DimmingOption,default= 1,verbose_name="Dimming")#
    orderitem_lm = models.CharField( "LM", max_length=60, null=False, blank=False)#
    orderitem_image = models.ImageField( "Image", null=True, blank=True, height_field="orderitem_height_field", width_field="orderitem_width_field")
    orderitem_height_field = models.IntegerField( null=True, blank=True, default=0)
    orderitem_width_field = models.IntegerField( null=True, blank=True, default=0)


    class Meta:
        ordering = ( 'product', )


    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


    def get_absolute_url(self):
        return reverse('quoted:orderitem_detail',args=[self.id])
