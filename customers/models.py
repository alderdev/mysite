from django.db import models
from django.core.urlresolvers import reverse





#客戶
class Customer(models.Model):
    sap_no = models.CharField(primary_key=True, max_length=18) # SAP客尸編號 -9223372036854775808 to 9223372036854775807
    title = models.CharField(max_length=36, null=False, blank=False)
    address = models.CharField( max_length=100, null=True, blank=True)
    #contact = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    #phone_ext = models.CharField(max_length=100, null=True, blank=True)
    faxno = models.CharField(max_length=100, null=True, blank=True)
    #email = models.EmailField(max_length=100, null=True, blank=True)
    invalid = models.BooleanField(default=False)#作廢

    create_at = models.DateTimeField(auto_now_add=True, auto_now =False)
    modify = models.DateTimeField(auto_now_add=False, auto_now =True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse( "customers:detail", kwargs={"pk": self.sap_no} )




class Contact(models.Model):
    customer = models.ForeignKey(Customer)
    master = models.BooleanField( default=False ) # default Contact person
    name = models.CharField(max_length=60, null=False, blank=False)
    job = models.CharField(max_length=60, null=False, blank=False)
    email = models.EmailField( null=True, blank= True)
    extention = models.CharField( max_length=8,null=True, blank= True )
    invalid = models.BooleanField(default=False)#作廢

    class Meta:
        ordering = ['-master']


    def __str__(self):
        return self.name
