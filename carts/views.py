from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Cart, CartItems
from quoted.models import Product
from django.core.urlresolvers import reverse



# Create your views here.
class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "carts/view.html"

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(300)
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id

        cart = Cart.objects.get(id = cart_id)

        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart


    def get(self, request, *args, **kwargs):
        cart = self.get_object()

        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete")
        if item_id:
            product_instance = get_object_or_404( Product, id=item_id )
            qty = request.GET.get("quantity")
            price = request.GET.get("price")
            qty1 = request.GET.get("quantity1")
            price1 = request.GET.get("price1")
            qty2 = request.GET.get("quantity2")
            price2 = request.GET.get("price2")
            qty3 = request.GET.get("quantity3")
            price3 = request.GET.get("price3")
            carts_item = CartItems.objects.get_or_create(cart=cart, item=product_instance)[0]
            if delete_item:
                carts_item.delete()
            else:
                carts_item.quantity = qty
                carts_item.price = price
                carts_item.quantity1 = qty1
                carts_item.price1 = price1
                carts_item.quantity2 = qty2
                carts_item.price2 = price2
                carts_item.quantity3 = qty3
                carts_item.price3 = price3
                carts_item.save()
                #print(carts_item)
        context = {
            "object":self.get_object()
        }
        template = self.template_name
        return render(request, template, context)



class ItemCountView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return JsonResponse({"count":10})
        else:
            raise Http404()
