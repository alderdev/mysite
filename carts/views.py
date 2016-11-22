from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Cart, CartItems
from quoted.models import Product


# Create your views here.
class CartView(View):

    def get(self, request, *args, **kwargs):
        item_id = request.GET.get("item")
        delete_item = requesy.GET.get("delete")
        if item_id:
            product_instance = get_object_or_404( Product, id=item_id )
            qty = request.GET.get("quantity")
            price = request.GET.get("price")
            qty1 = request.GET.get("quantity1")
            price1 = request.GET.get("price")
            qty2 = request.GET.get("quantity2")
            price2 = request.GET.get("price")
            qty3 = request.GET.get("quantity3")
            price3 = request.GET.get("price")

            carts = Carts.objects.all().first()
            carts_item = CartItems.objects.get_or_create(cart=carts, item=product_instance)[0]
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
        return HttpResponseRedirect("/")



class ItemCountView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return JsonResponse({"count":10})
        else:
            raise Http404()
