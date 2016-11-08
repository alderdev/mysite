from django.conf import settings
from quoted.models import Product
from decimal import Decimal
#from shop.models import Product

class Cart(object):

    def __init__(self,request):
        """
            Initialize the Cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID]={}

        self.cart = cart


    def add( self, product, quantity, price, quantity1, price1, quantity2, price2, quantity3, price3, update_quantity=False ):
        """
            Add in product to The Cart
        """

        #print("quantity3"+ quantity3)
        #print("price3" +price3)
        qty = quantity
        pce = price
        qty1 = quantity1
        pce1 = price1
        qty2 = quantity2
        pce2 = price2
        qty3 = quantity3
        pce3 = price3


        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]={
                'quantity':quantity,
                'price':price,

                'quantity1':quantity1,
                'price1':price1,
                'quantity2':quantity2,
                'price2':price2,
                'quantity3':quantity3,
                'price3':price3

                 }

        # if update_quantity:
        #     print("update_quantity is True")
        #     self.cart[product_id]['quantity'] = quantity
        # else:
        #     print("update_quantity is False")
        #     self.cart[product_id]['quantity'] += quantity

        self.save()


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


    def remove(self,product ):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            #print(item)
            item['quantity'] = item['quantity']
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item


    def __len__(self):
        """
        Cart all Item Count
        """
        return sum( item['quantity'] for item in self.cart.values() )


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
