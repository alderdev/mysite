from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Product, OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q

def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,'quoted/product/list.html',locals() )


def product_detail(request, id, slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_product_form = CartAddProductForm()
    #return render(request,    'shop/product/detail.html',    {'product': product,    'cart_product_form': cart_product_form})

    return render(request,'quoted/product/detail.html',locals() )



def order_create(request):

    cart = Cart(request)
    form = OrderCreateForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():

            form.instance.order_number = Order.objects.month_sequence()
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
            cart.clear()
            return HttpResponseRedirect( '../' )


        return render(request,'quoted/product/list.html',locals())


    return render(request,'quoted/order_form.html',locals())


class OrderList(ListView):
    model = Order
    paginate_by = 10



#顯示和列印共用
class OrderDetail(DetailView):
    model = Order


from django.template.loader import render_to_string
def order_print(request, id):
    order = get_object_or_404(Order,id=id)
    html = render_to_string('quoted/order_print.html',{'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\"order_{}.pdf"'.format(order.id)

    return response
