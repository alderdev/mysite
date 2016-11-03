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
    c.drawImage(footer_line, 20, 805, mask='auto', width=490,height=20)
    c.drawImage(upline, 40, 25, mask='auto', width=500,height=20)



    c.setTitle("Alder Optomechanical Corp.")
    c.setSubject("Quotation")
    c.drawImage(logo, 525, 780, mask='auto', width=45,height=45)
    c.setFont("simhei", 24)
    c.drawString(150, 780, "Alder Optomechanical Corp.")
    c.setFont("simhei", 22)
    c.drawString(250, 760, "Quotation")

    c.setFont("simhei", 10)
    # Report Field lable
    y = 745
    x = 100
    #Header left
    c.drawRightString(x,y ,"Quote Number " + ":")
    c.drawRightString(x,y-15, "Customer " + ":")
    c.drawRightString(x,y-30, "Contact Person " + ":")
    c.drawRightString(x,y-45, "Contact Email " + ":")
    c.drawRightString(x,y-60, "Payment Term " + ":")
    c.drawRightString(x,y-75, "Price Term " + ":")

    #Header Right
    c.drawRightString(x+350,y, "Sales Contact " + ":")
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
    c.drawString( x_position, y_position +25, "Product Name / Model Name / Description" )
    #c.drawString( x_position +200, y_position +25, "Product Name" )
    #c.drawString( x_position +300, y_position +25, "WATT" )
    c.drawString( x_position +400, y_position +25, "Quantity" )
    c.drawString( x_position +450, y_position +25, "Price" )
    c.line(25,640,570,640)
    c.line(25,615,570,615)

    for item in order.orderitem_set.all():
        c.drawString( 25, y_position, str(number)+ ". " )

        imageurl = settings.MEDIA_ROOT+"/" +str(item.product.image.url).split("/")[2]
        c.drawImage(imageurl, 40, y_position-25, mask='auto', width=35,height=35)

        c.drawString( x_position, y_position, item.product.name )
        c.drawString( x_position, y_position-12, item.product.modelname )

        c.drawString( x_position, y_position-24, "Watt: " + item.product.watt + ",  CRI:" + item.product.cri + ",  CCT:" + item.product.cct  )
        c.drawRightString( x_position +400, y_position, str(item.quantity) )
        c.drawRightString( x_position +480, y_position, str(item.price) )

        y_position -= 40
        number += 1




    c.drawRightString( 60, y_position-25, "Remark :")
    remark_obj = c.beginText(60 , y_position - 40)
    remark_obj.textLines(order.comment)
    c.drawText( remark_obj )

    yp = remark_obj.getY()






    c.showPage()
    c.save()
    return response





# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_RIGHT
# from django.contrib.auth.models import User
#
# @staticmethod
# def _header_footer(canvas, doc):
#     # Save the state of our canvas so we can draw on it
#     canvas.saveState()
#     styles = getSampleStyleSheet()
#
#     # Header
#     header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
#     w, h = header.wrap(doc.width, doc.topMargin)
#     header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
#
#     # Footer
#     footer = Paragraph('This is a multi-line footer.  It goes on every page.   ' * 5, styles['Normal'])
#     w, h = footer.wrap(doc.width, doc.bottomMargin)
#     footer.drawOn(canvas, doc.leftMargin, h)
#
#     # Release the canvas
#     canvas.restoreState()




# 測試V2





from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "Alder Optomechanical Corp."
Subject = "Quotation"
pageinfo = "platypus example"
logo = settings.STATIC_ROOT +"/img/alder_logo.png"
upline = settings.STATIC_ROOT +"/img/alder_upline.jpg"
footer_line = settings.STATIC_ROOT +"/img/footer_line.jpg"
pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('VeraBd', 18)
    canvas.drawImage(upline, 25, 25, mask='auto', width=490,height=20)
    canvas.drawImage(footer_line, 25, 805, mask='auto', width=540,height=20)
    canvas.drawImage(logo, PAGE_WIDTH/4.8,PAGE_HEIGHT-250, mask='auto', width=45,height=45)
    canvas.drawCentredString(PAGE_WIDTH/1.9,PAGE_HEIGHT-250, Title )
    canvas.drawCentredString(PAGE_WIDTH/2.0,PAGE_HEIGHT-270, Subject )
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(530, 0.45 * inch, "First Page" )
    canvas.restoreState()

def myLaterPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('VeraBd', 9)
    contact_info = "Alder Optomechanical Corp."
    canvas.drawString(30, 795 ,  contact_info  )
    canvas.setFont('Times-Roman', 9)
    canvas.drawImage(logo, 530,780, mask='auto', width=45,height=45)
    canvas.drawString(530, 0.45 * inch, "Page %d " % ( doc.page) )
    #canvas.drawString(inch, 0.45 * inch, "Page %d %s" % ( doc.page, pageinfo) )
    canvas.drawImage(footer_line, 25, 805, mask='auto', width=490,height=20)
    contact_address = "No.171 Tianjin Street, Pignzhen Dist., Taoyuan City 32458, Taiwan. \b www.alder.com.tw \n sales@alder.com.tw \n +886-3-4393588"
    canvas.drawString(30, 785 ,  contact_address )
    canvas.drawImage(upline, 25, 25, mask='auto', width=490,height=20)
    canvas.restoreState()



def _generate_pdf(course, output):
    from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table , TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm, inch
    from reportlab.lib import colors
    from reportlab.platypus import XPreformatted
    from django.conf import settings
    from reportlab.pdfgen import canvas
    pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
    #from cStringIO import StringIO

    doc = SimpleDocTemplate(output,pagesize=A4,
    rightMargin=.5*inch,leftMargin=.5*inch,
    topMargin=inch,bottomMargin=.6*inch)


    Story = [Spacer(1, 3.5*inch)]
    style = styles["Normal"]
    styleN = styles['Normal']
    styleH = styles['Heading1']


    comment = Paragraph('''
       <para align=left spaceb=3>'''+ course.comment +'''</para>''',
       styles["BodyText"])

    #頁首的資訊
    header = [['Quotation No:', course.order_number,'                                '],
              ['ATTN:', course.customer.title,'                                '],
              ['Contact:', course.contact.name,''],
              ['Email:', course.email,''],
              ['Currency:', course.currency,''],
              ['Payment Term:', course.paymentterm,''],
              ['Price Term:', course.priceterm,''],
              ['Date:', course.ord_date,''],
              ['Expired Date:', course.effective_date,''],
              ['Remark:', comment,''],

              ]

    h = Table(header,style=[
                        ('ALIGN',(0,0),(0,-1), 'RIGHT'),
                        ('FONTNAME', (1,0),(1,-1), 'simhei'),
                        ('SPAN',(1,-1),(2,-1)),
                        ('VALIGN',(0,0),(0,-1),'TOP'),
                    ])

    Story.append(h)

    Story.append(PageBreak())


    element = []
    tableheader = ['No.','Image', 'Product / Model Name  / Description                                                                   ', 'Quantity' ,'Price']
    element.append(tableheader)
    loopcounter = 1
    for item in course.orderitem_set.all():

        myitem = []
        myitem.append( loopcounter )
        img = settings.MEDIA_ROOT+"/" +str(item.product.image.url).split("/")[2]
        I = Image(img)
        I.drawHeight = 0.55*inch
        I.drawWidth = 0.55*inch

        myitem.append( I )
        desctiption = "Watt: "+ str(item.product.watt) + " , Option1:" + item.product.option1 + " , Beam Angle:" + item.product.beam_angle + ' , CRI: ' + str(item.product.cri) + ' , CCT: ' +item.product.cct




        myitem.append( item.product.name + '\n' +desctiption + '\nDimming Option:'+ str(item.product.dimming) + '\nModel No.: '+ item.product.modelname )

        #myitem.append( item.product.watt )
        #myitem.append( item.product.cct )
        #myitem.append( item.product.cri )
        myitem.append( item.quantity )
        myitem.append( '$ '+str(item.price) )

        element.append(myitem)
        loopcounter += 1


    t = Table(element)

    t.setStyle(
        TableStyle(
            [('BACKGROUND',(0,0),(4,0),colors.skyblue),
             ('ALIGN',(0,0),(3,0),'CENTER'),
             ('SIZE',(2,1),(2,-1), 8),

             ('VALIGN',(0,0),(4,-1),'TOP'),
             ('ALIGN',(3,0),(4,-1), 'RIGHT'),
             ('TEXTCOLOR',(3,1),(4,-1), colors.blue),
             ]
        )
    )
    # t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
    #                    ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
    #                    ('VALIGN',(0,0),(0,-1),'TOP'),
    #                    ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
    #                    ('ALIGN',(0,-1),(-1,-1),'CENTER'),
    #                    ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
    #                    ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
    #                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    #                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    #                    ]))



    Story.append(t)



    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPage )



def gen_pdfv2(request,id):
    response = HttpResponse(content_type='application/pdf')
    filename = '-outline.pdf'
    response['Content-Disposition'] = 'filename=' + filename
    course = get_object_or_404(Order,id=id)
    _generate_pdf(course, response)

    return response
