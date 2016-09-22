from django.db import models
from django.utils import timezone
from customers.models import Customer
from products.models import Product
from django.core.urlresolvers import reverse



#自訂單據號碼
class OrderNumberManager(models.Manager):

    #短的月份序號如：16080001
    def short_month_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(create_at__contains = order_date[:7] ).count()+1
        order_number = nextNumber + int(order_date[2:7].replace('-',''))*10000
        return order_number
    #月份序號如：2016080001
    def month_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(create_at__contains = order_date[:7] ).count()+1
        order_number = nextNumber + int(order_date[:7].replace('-',''))*10000
        return order_number
    #月份序號如：2016080001
    def day_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(create_at__contains = order_date ).count()+1
        order_number = nextNumber + int(order_date.replace('-',''))*10000
        return order_number
    #短的日序號如：1608310001
    def short_day_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(create_at__contains = order_date ).count()+1
        order_number = nextNumber + int(order_date.replace('-','')[2:])*10000
        return order_number


class OrderLineManager(models.Manager):

    #短的月份序號如：16080001
    def currency_number(self):

        currencyNumber = self.filter( quotehead = self.quotehead ).count()+10

        return currencyNumber


#幣別
class Currency(models.Model):
    code = models.CharField(primary_key=True, max_length=3, )
    description = models.CharField(max_length=36, null=False, blank=False)

    def __str__(self):
        return self.code


# 報價單
class QuoteHead(models.Model):
    request_user = models.CharField(max_length=60, null=False, blank=False) #開單人
    order_number = models.CharField(max_length=12, null=True, blank=True, unique=True) #報價單號
    ord_date = models.DateField(default=timezone.now) #報價日期
    customer = models.ForeignKey(Customer) #客戶編號
    effective_date = models.DateField( default=timezone.now ) # 報價單有效日期
    currency = models.ForeignKey( Currency )
    invalid = models.BooleanField(default=False) #作廢
    comment = models.TextField(null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True, auto_now =False)
    modify = models.DateTimeField(auto_now_add=False, auto_now =True)

    objects = OrderNumberManager()
    def __str__(self):
        return self.order_number


    def get_absolute_url(self):
        return reverse( "quotations:detail", kwargs={"pk": self.id} )



# 報價單明細
class QuoteDetail(models.Model):
    quotehead = models.ForeignKey(QuoteHead) #報價單編號
    line_no = models.IntegerField() #行號
    product = models.ForeignKey(Product) # 料號
    unit_price = models.FloatField() # 單價
    line_memo = models.CharField(max_length=50, blank=True, null=True) # 行備註
    invalid = models.BooleanField(default=False) #作廢

    create_at = models.DateTimeField(auto_now_add=True, auto_now =False)
    modify = models.DateTimeField(auto_now_add=False, auto_now =True)

    def __str__(self):
        return self.product.part_number


    def get_absolute_url(self):
        return reverse( "quotations:detail", kwargs={"pk": self.id} )
