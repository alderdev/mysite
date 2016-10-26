from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Product, OrderItem, Order
from .forms import OrderCreateForm,OrderUpdateForm, OrderItemForm
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


from django.contrib import admin

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

inlines = [OrderItemInline]

def order_create(request):

    cart = Cart(request)
    form = OrderCreateForm(request.POST or None)
    #raw_id_fields = ['customer']
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


    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query_list = Order.objects.filter(
                Q(order_number=query)
            ).distinct()
            return query_list

        return Order.objects.filter(is_valid=True)








def order_detail(request, id):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    order = get_object_or_404(Order,id=id)
    orderitem_form = OrderItemForm()

    return render(request,'quoted/order_detail.html',locals() )



#顯示和列印共用
class OrderDetail(DetailView):
    model = Order

from django.conf import settings
from django.template.loader import render_to_string
import weasyprint


class OrderUpdate(UpdateView):
    model = Order
    fields = ['is_valid','customer', 'contact', 'email', 'currency', 'paymentterm', 'priceterm', 'quote_sales','ord_date', 'effective_date','comment']
    form_clss = OrderUpdateForm()



def order_print(request, id):

    order = get_object_or_404(Order,id=id)
    html = render_to_string('quoted/order_print.html',{'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\"order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html, base_url = request.build_absolute_uri() ).write_pdf(response,stylesheets=[weasyprint.CSS( settings.STATIC_ROOT + '/css/pdf.css')])

    return response




def quote_delete_item(request, id):

    #print( request.POST.get['order_id'] )
    if request.POST or None:
        rq = request.POST.getlist('rows')

        instance = OrderItem.objects.filter(id__in= rq )
        instance.delete()
        return HttpResponseRedirect("../")
        #return HttpResponseRedirect("../%s" %str(request.POST['order_id']))

    return render(request, "../%s" %str(request.POST['order_id']), locals())


def order_item_insert(request):

    if request.method=='POST':
        order_id = request.POST['order_id']
        product_id = request.POST['product_id']
        price = request.POST['price']
        quantity = 1

        OrderItem.objects.create(
            order_id = order_id,
            product_id = product_id,
            price = price,
            quantity = quantity
        )

    return HttpResponse()


#use ReportLab
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm , letter

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.utils import ImageReader
from django.contrib.staticfiles.templatetags.staticfiles import static

def gen_pdf(request,id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="genReport.pdf"'
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

    #print(pdfmetrics.getRegisteredFontNames())

    order = get_object_or_404(Order,id=id)
    order_number = order.order_number

    logo = ImageReader('http://www.alder.com.tw/Content/Images/logo.gif')







    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    c.setTitle("Alder Optomechanical Corp.")
    c.setSubject("Quotation")
    c.drawImage(logo, 90, 780, mask='auto', width=45,height=45)
    c.setFont("simhei", 24)
    c.drawString(150, 800, "Alder Optomechanical Corp.")
    c.setFont("simhei", 22)
    c.drawString(250, 780, "Quotation")

    c.setFont("simhei", 8)
    # Report Field lable
    y = 745
    x = 100

    c.drawRightString(x,y ,"Order Number " + ":")
    c.drawRightString(x,y-15, "Customer " + ":")
    c.drawRightString(x,y-30, "Contact Person " + ":")
    c.drawRightString(x,y-45, "Contact Email " + ":")
    c.drawRightString(x,y-60, "Payment Term " + ":")
    c.drawRightString(x,y-75, "Price Term " + ":")

    c.drawRightString(x+350,y, "Sales Name " + ":")
    c.drawRightString(x+350,y-15, "Effective Date " + ":")
    c.drawRightString(x+350,y-30, "Quote Date " + ":")
    c.drawRightString(x+350,y-45, "Currency " + ":")


    # Django Field
    c.drawString(x +5, y, order_number )
    c.drawString(x +5, y-15, order.customer.title )
    c.drawString(x +5, y-30, order.contact.name )
    c.drawString(x +5, y-45, order.email )
    c.drawString(x +5, y-60, order.paymentterm.description )
    c.drawString(x +5, y-75, order.priceterm.description )

    #c.drawDate(x +5, y-90, order.ord_date )
    #c.drawDate(x +5, y-105, order.effective_date )
    c.drawString(x +355, y, order.quote_sales )
    c.drawString(x +355, y-45, order.currency.code )



    #c.setFont("STSong-Light", 10)


    y_position = 650
    for item in order.orderitem_set.all():
        #img = static( item.product.image.url )
        #c.drawImage( img, 30, y_position, mask='auto', width=45,height=45)
        #c.drawImage(item.product.image.url, 30, y_position, mask='auto', width=45,height=45)
        c.drawImage(logo, 40, y_position-25, mask='auto', width=30,height=30)
        c.drawString( 100, y_position, item.product.modelname )
        c.drawString( 100+200, y_position, item.product.name )
        c.drawString( 100+300, y_position, item.product.watt )
        c.drawString( 100+350, y_position, item.product.cri )
        c.drawString( 100+400, y_position, item.product.cct )
        y_position -= 35




    c.showPage()
    c.save()
    return response
