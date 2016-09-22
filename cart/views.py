
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from prod_model.models import ProdModel
from .cart import Cart
from .forms import CartAddProdmodelForm

@require_POST
def cart_add(request, prodmodel_id):
    cart = Cart(request)
    product = get_object_or_404(ProdModel, id=prodmodel_id)
    form = CartAddProdmodelForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'],update_quantity=cd['update'])

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
