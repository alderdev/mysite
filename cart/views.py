from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from quoted.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request):
    #print("cart_add")
    product_id = request.POST['product_id']
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id )
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        #print("is_valid")
        cd = form.cleaned_data
        cart.add( product=product
        ,quantity=cd['quantity'],price=cd['price']
        ,quantity1=cd['quantity1'],price1=cd['price1']
        ,quantity2=cd['quantity2'],price2=cd['price2']
        ,quantity3=cd['quantity3'],price3=cd['price3']
        ,update_quantity=cd['update'])

    #return redirect('quoted:product_list')
    return HttpResponse()




def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404( Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
