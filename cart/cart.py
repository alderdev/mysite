from django.conf import settings
from prod_model.models import ProdModel

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

    def add(self,prodmodel, quantity=1, update_quantity=False ):
        """
            Add in ProdModel to The Cart
        """
        prodmodel_id = str(prodmodel.id)
        if prodmodel_id not in self.cart:
            self.cart[prodmodel_id]={
                'quantity':0,
            }

        if update_quantity:
            self.cart[prodmodel_id]['quantity'] = quantity
        else:
            self.cart[prodmodel_id]['quantity'] += quantity

        self.save()


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


    def remove(self,prodmodel ):
        prodmodel_id = str(prodmodel.id)
        if prodmodel_id in cart:
            del self.cart[prodmodel_id]
            self.save()

    def __iter__(self):
        prodmodel_ids = self.cart.keys()
        prodmodels = Prodmodel.objects.filter(id__in=prodmodel_ids)
        for prodmodel in prodmodels:
            self.cart[str(prodmodel.id)]['prodmodel'] = prodmodel

        for item in self.cart.values():
            item['quantity'] = item['quantity']


    def __len__(self):
        """
        Cart all Item Count
        """
        return sum( item['quantity'] for item in self.cart.values() )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
