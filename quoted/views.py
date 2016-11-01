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
        quantity = request.POST['quantity']
        #因為單價有可能不一樣,所以不考慮將相同品項的數量加總
        #print("OrderID: %s, ProductId: %s"  %(order_id,product_id))
        instance = OrderItem.objects.filter(order_id= order_id, product_id__in= product_id, price=price)
        if instance:
            pass
            #print("Exists True")
        else:
            pass
            #print("Not Exists")


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

    #logo = ImageReader('http://www.alder.com.tw/Content/Images/logo.gif')
    logo = settings.STATIC_ROOT +"/img/alder_logo.png"

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4


    upline = settings.STATIC_ROOT +"/img/alder_upline.jpg"
    footer_line = settings.STATIC_ROOT +"/img/footer_line.jpg"
    c.drawImage(footer_line, 80, 805, mask='auto', width=490,height=20)
    c.drawImage(upline, 40, 25, mask='auto', width=500,height=20)



    c.setTitle("Alder Optomechanical Corp.")
    c.setSubject("Quotation")
    c.drawImage(logo, 25, 780, mask='auto', width=45,height=45)
    c.setFont("simhei", 24)
    c.drawString(150, 780, "Alder Optomechanical Corp.")
    c.setFont("simhei", 22)
    c.drawString(250, 760, "Quotation")

    c.setFont("simhei", 8)
    # Report Field lable
    y = 745
    x = 100
    #Header left
    c.drawRightString(x,y ,"Order Number " + ":")
    c.drawRightString(x,y-15, "Customer " + ":")
    c.drawRightString(x,y-30, "Contact Person " + ":")
    c.drawRightString(x,y-45, "Contact Email " + ":")
    c.drawRightString(x,y-60, "Payment Term " + ":")
    c.drawRightString(x,y-75, "Price Term " + ":")

    #Header Right
    c.drawRightString(x+350,y, "Sales Name " + ":")
    c.drawRightString(x+350,y-15, "Sales Email " + ":")
    c.drawRightString(x+350,y-30, "Quote Date " + ":")
    c.drawRightString(x+350,y-45, "Effective Date " + ":")
    c.drawRightString(x+350,y-60, "Currency " + ":")


    # Django Field
    c.drawString(x +5, y, order_number )
    c.drawString(x +5, y-15, order.customer.title )
    c.drawString(x +5, y-30, order.contact.name )
    c.drawString(x +5, y-45, order.email )
    c.drawString(x +5, y-60, order.paymentterm.description )
    c.drawString(x +5, y-75, order.priceterm.description )

    c.drawString(x +355, y, order.quote_sales )
    c.drawString(x +355, y-15, "sales@alder.com.tw" )
    c.drawString(x +355, y-30, str(order.ord_date) )
    c.drawString(x +355, y-45, str(order.effective_date) )
    c.drawString(x +355, y-60, order.currency.code )



    #c.setFont("STSong-Light", 10)

    x_position = 80
    y_position = 600
    number = 1

    c.drawString( 25, y_position +25, "No." )
    c.drawString( 45, y_position +25, "Images" )
    c.drawString( x_position, y_position +25, "Model Name" )
    c.drawString( x_position +200, y_position +25, "Product Name" )
    c.drawString( x_position +300, y_position +25, "WATT" )
    c.drawString( x_position +350, y_position +25, "CRI" )
    c.drawString( x_position +400, y_position +25, "CCT" )
    c.line(25,640,570,640)
    c.line(25,615,570,615)

    for item in order.orderitem_set.all():
        c.drawString( 25, y_position, str(number)+ ". " )

        imageurl = settings.MEDIA_ROOT+"/" +str(item.product.image.url).split("/")[2]
        c.drawImage(imageurl, 40, y_position-25, mask='auto', width=30,height=30)

        #c.drawString( 100, y_position-10, imageurl )
        #print( str(item.product.image.url).split("/")[2] )
        c.drawString( x_position, y_position, item.product.modelname )
        c.drawString( x_position +200, y_position, item.product.name )
        c.drawString( x_position +300, y_position, item.product.watt )
        c.drawString( x_position +350, y_position, item.product.cri )
        c.drawString( x_position +400, y_position, item.product.cct )

        y_position -= 35
        number += 1

    print(y_position)


    c.drawRightString( 60, y_position-25, "Remark :")
    remark_obj = c.beginText(60 , y_position - 40)
    remark_obj.textLines(order.comment)
    c.drawText( remark_obj )

    yp = remark_obj.getY()
    print(yp)






    c.showPage()
    c.save()
    return response





from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from django.contrib.auth.models import User

@staticmethod
def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    styles = getSampleStyleSheet()

    # Header
    header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

    # Footer
    footer = Paragraph('This is a multi-line footer.  It goes on every page.   ' * 5, styles['Normal'])
    w, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, h)

    # Release the canvas
    canvas.restoreState()



def gen_pdfv2(request,id):
    # Register Fonts
    pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
    #pdfmetrics.registerFont(TTFont('Arial', settings.STATIC_ROOT + 'fonts/arial.ttf'))
    #pdfmetrics.registerFont(TTFont('Arial-Bold', settings.STATIC_ROOT + 'fonts/arialbd.ttf'))

    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()
    # Our Custom Style
    styles.add(ParagraphStyle(name='RightAlign', fontName='helvetica', align=TA_RIGHT))



    #buffer = self.buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=A4)

        # Our container for 'Flowable' objects
    elements = []

        # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='RightAlign', fontName='helvetica' ,alignment=TA_RIGHT))

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
    users = User.objects.all()
    elements.append(Paragraph('My User Names', styles['RightAlign']))
    for i, user in enumerate(users):
        elements.append(Paragraph(user.get_full_name(), styles['Normal']))

    doc.build(elements, onFirstPage= _header_footer, onLaterPages= _header_footer,
                  canvasmaker=NumberedCanvas)

        # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()



    return pdf





class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(200*mm, 20*mm,
            "Page %d of %d" % (self._pageNumber, page_count))
