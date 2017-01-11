from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Product, OrderItem, Order, GeneralTerm
from .forms import OrderCreateForm,OrderUpdateForm, OrderItemForm, OrderItemUpdateForm
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.views.generic.detail import  DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.decorators import login_required



class ProductList(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super( ProductList, self).get_context_data(*args, **kwargs )
        context['categories'] = Category.objects.all()
        #print(context)
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'quoted/product/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetail, self).get_context_data(*args, **kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context



@login_required
def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    product_list = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product_list = product_list.filter(category=category)

    return render(request,'quoted/product/product_list.html',locals() )


def product_detail(request, id, slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)


    if product.productprice_set.all().first() is not None:
        usd_price = product.productprice_set.all().first().std_price
        cart_product_form = CartAddProductForm({"quantity":1, "price":usd_price })
    else:
        cart_product_form = CartAddProductForm()

    #return render(request,    'shop/product/detail.html',    {'product': product,    'cart_product_form': cart_product_form})

    return render(request,'quoted/product/product_detail.html',locals() )




class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

inlines = [OrderItemInline]


def order_create(request):

    cart = Cart(request)
    form = OrderCreateForm(request.POST or None)
    order_session_id =  request.user.id

    #raw_id_fields = ['customer']
    if request.method == 'POST':

        if form.is_valid():

            form.instance.order_number = Order.objects.month_sequence()
            form.instance.quote_sales = request.user.username
            form.instance.quote_user = request.user

            order = form.save()
            for item in cart:

                OrderItem.objects.create(
                        order_id = order.id,
                        product_id = item['product'].id,
                        price = item['price'],
                        quantity = item['quantity'],

                        price1 = item['price1'],
                        quantity1 = item['quantity1'],
                        price2 = item['price2'],
                        quantity2 = item['quantity2'],
                        price3 = item['price3'],
                        quantity3 =item['quantity3'],

                        orderitem_name = item['product'].name,
                        orderitem_modelname = item['product'].modelname,
                        orderitem_option1 = item['product'].option1,
                        orderitem_beam_angle = item['product'].beam_angle,
                        orderitem_cri = item['product'].cri,
                        orderitem_cct = item['product'].cct,
                        orderitem_watt = item['product'].watt,
                        orderitem_lm = item['product'].lm,
                        orderitem_image = item['product'].image,
                        orderitem_dimming_id = item['product'].dimming.id
                        )

            cart.clear()
            return HttpResponseRedirect( '../' )

        return render(request,'quoted/order_form.html',locals())

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




class OrderDetail(DetailView):
    model = Order



#Quote Items DetailView
class OrderItemDetail(UpdateView):
    model = OrderItem
    form_clss = OrderItemUpdateForm
    fields = [
                'is_special',
                'orderitem_name',
                'orderitem_modelname',
                'orderitem_option1',
                'orderitem_beam_angle',
                'orderitem_cct',
                'orderitem_dimming',
                'orderitem_cri',
                'orderitem_watt',
                'orderitem_lm',
                'orderitem_image',
                'quantity',
                'price',
                'quantity1',
                'price1',
                'quantity2',
                'price2',
                'quantity3',
                'price3',
                'line_remark'
             ]
    #success_url = reverse_lazy("quoted:detail",args=[self.order_id])









from django.conf import settings
from django.template.loader import render_to_string
#import weasyprint



class OrderUpdate(UpdateView):
    model = Order
    fields = ['is_valid','customer', 'contact', 'email', 'currency', 'paymentterm', 'priceterm', 'quote_sales','ord_date', 'effective_date','comment']
    form_clss = OrderUpdateForm()




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

        price1 = request.POST['price1']
        quantity1 = request.POST['quantity1']
        price2 = request.POST['price2']
        quantity2 = request.POST['quantity2']
        price3 = request.POST['price3']
        quantity3 = request.POST['quantity3']

        if request.POST['price1'] =='':
            price1 = None
            quantity1 = None
            #print("['price1'] is not None")

        if request.POST['price2'] =='':
            price2 = None
            quantity2 = None
            #print("['price2'] is not thing")

        if request.POST['price3'] =='':
            price3 = None
            quantity3 = None
            #print("['price3'] is not thing")

        #因為單價有可能不一樣,所以不考慮將相同品項的數量加總
        #print("OrderID: %s, ProductId: %s"  %(order_id,product_id))
        instance = OrderItem.objects.filter(order_id= order_id, product_id__in= product_id, price=price)



        product_obj = get_object_or_404(Product, id=product_id)

        #print(product_obj.dimming)

        OrderItem.objects.create(
                order_id = order_id,
                product_id = product_id,
                price = price,
                quantity = quantity,

                price1 = price1,
                quantity1 = quantity1,
                price2 = price2,
                quantity2 = quantity2,
                price3 = price3,
                quantity3 = quantity3,


                orderitem_name = product_obj.name,
                orderitem_modelname = product_obj.modelname,
                orderitem_option1 = product_obj.option1,
                orderitem_beam_angle = product_obj.beam_angle,
                orderitem_cri = product_obj.cri,
                orderitem_cct = product_obj.cct,
                orderitem_watt = product_obj.watt,
                orderitem_lm = product_obj.lm,
                orderitem_image = product_obj.image,
                orderitem_dimming_id = 1
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




# 正式Quote-A

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "Alder Optomechanical Corp."
Subject = "Quotation"

logo = settings.STATIC_ROOT +"/img/alder_logo.png"
upline = settings.STATIC_ROOT +"/img/alder_upline.jpg"
footer_line = settings.STATIC_ROOT +"/img/footer_line.jpg"
#factory_img = settings.STATIC_ROOT +"/img/factory.png"
certification_img = settings.STATIC_ROOT +"/img/certification.png"
pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

# 封面的Layout

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('VeraBd', 18)
    canvas.drawImage(upline, 25, 25, mask='auto', width=490,height=20)
    canvas.drawImage(footer_line, 25, 805, mask='auto', width=540,height=20)
    #canvas.drawImage(logo, PAGE_WIDTH/5.2,PAGE_HEIGHT-252, mask='auto', width=55,height=45)
    canvas.drawImage(logo, PAGE_WIDTH/2.2,PAGE_HEIGHT-200, mask='auto', width=55,height=45)
    canvas.drawImage( certification_img, 45, 55, mask='auto', width=495,height=45 )
    canvas.drawCentredString(PAGE_WIDTH/2.0,PAGE_HEIGHT-235, Title )
    canvas.setFont('VeraBd', 20)
    canvas.drawCentredString(PAGE_WIDTH/2.0,PAGE_HEIGHT-310, Subject )
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(530, 0.45 * inch, "First Page" )
    canvas.restoreState()



def myLaterPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('VeraBd', 9)
    contact_info = "Alder Optomechanical Corp."

    canvas.setFont('Times-Roman', 9)
    canvas.drawImage(logo, 520,780, mask='auto', width=55,height=45)
    canvas.drawString(530, 0.45 * inch, "Page %d " % ( doc.page) )
    #canvas.drawString(inch, 0.45 * inch, "Page %d %s" % ( doc.page, pageinfo) )
    canvas.drawImage(footer_line, 25, 805, mask='auto', width=485,height=20)
    contact_address = "No.171 Tianjin Street, Pignzhen Dist., Taoyuan City 32458, Taiwan.    www.alder.com.tw    sales@alder.com.tw    +886-3-4393588"

    # 地址放在上面的圖騰下
    canvas.setFont('VeraBd', 9)
    canvas.drawString(30, 795 ,  contact_info  )
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(30, 785 ,  contact_address )
    canvas.drawImage(upline, 25, 25, mask='auto', width=490,height=20)

    # 地址放在下面的圖騰下
    # canvas.setFont('VeraBd', 9)
    # canvas.drawString(30, 40 ,  contact_info  )
    # canvas.setFont('Times-Roman', 9)
    # canvas.drawString(30, 25 ,  contact_address )
    # canvas.drawImage(upline, 25, 50, mask='auto', width=540,height=20)


    canvas.restoreState()


from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle,PropertySet
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib import colors
class ParagraphStyle(PropertySet):
    defaults = {
        'fontName':'Times-Roman',
        'fontSize':10,
        'leading':12,
        'leftIndent':0,
        'rightIndent':0,
        'firstLineIndent':12,
        'alignment':0,
        'spaceBefore':0,
        'spaceAfter':0,
        'bulletFontName':'Times-Roman',
        'bulletFontSize':10,
        'bulletIndent':0,
        'textColor': colors.black,
        'backColor':None,
        'wordWrap':None,
        'borderWidth': 0,
        'borderPadding': 0,
        'borderColor': None,
        'borderRadius': None,
        'allowWidows': 1,
        'allowOrphans': 0,
        'textTransform':None,
        'endDots':None,
        'splitLongWords':1,
        'underlineProportion': 0.0,
        'bulletAnchor': 'start',
        }


def _generate_pdf(course, output):
    from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table , TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle,PropertySet
    from reportlab.lib.units import mm, inch
    from reportlab.lib import colors
    from reportlab.platypus import XPreformatted, Preformatted
    from django.conf import settings
    from reportlab.pdfgen import canvas
    pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
    pdfmetrics.registerFont(TTFont('Arialuni', 'arialuni.ttf'))


    doc = SimpleDocTemplate(
        output,pagesize=A4,
        rightMargin=.5*inch,leftMargin=.5*inch,
        topMargin=inch,bottomMargin=.6*inch
    )


    Story = [Spacer(1, 3.5*inch)]
    style = styles["Normal"]
    styleN = styles['Normal']
    styleH = styles['Heading1']

    ###
    stylesheet=getSampleStyleSheet()
    normalStyle = stylesheet['Normal']

    #頁首的資訊
    header = [['Quotation No',':', course.order_number],
              ['Customer',':', course.customer.title],
              ['Contact Person',':', course.contact.name],
              ['Contact Email',':', course.contact.email],
              ['Date',':', course.ord_date],
              ['Expired Date',':', course.effective_date],
              ]

    h = Table(header,style=[
                            ('ALIGN',(0,0),(0,-1), 'LEFT'),
                            ('FONTNAME', (2,0),(2,-1), 'Arialuni'),
                            ('SPAN',(1,-1),(1,-1)),
                            ('VALIGN',(0,0),(0,-1),'TOP'),
                        ]
                )

    Story.append(h)

    Story.append(PageBreak())

    #因為要套用字型Arialuni, 所以將comment改為Paragraph
    comment = Paragraph('''
       <para align=left spaceb=3><font face="Arialuni">'''+ course.comment +'''</font></para>''',
       styles["BodyText"])

    #頁首的資訊
    header = [
              ['Quotation No',':', course.order_number,'','Date',':', course.ord_date],
              ['Customer',':', course.customer.title,'','Expired Date',':', course.effective_date],
              ['Contact Person',':', course.contact.name, '','Sales Contact',':', course.quote_user],
              ['Contact Email',':', course.contact.email,'', 'Email',':', course.quote_user.email],
              ['Payment Term',':', course.paymentterm,'','Currency',':' , course.currency],
              ['Price Term',':', course.priceterm,''],
              ]

    h = Table(header, colWidths=[1.0*inch, 0.1*inch, 2.8*inch, 0.3*inch, 0.9*inch, 0.1*inch, 2.0*inch] ,style=[
                        #('ALIGN',(0,0),(0,-1), 'LEFT'),
                        ('SPAN',(2,0),(3,0)),
                        ('FONTNAME', (2,0),(2,-1), 'Arialuni'),

                        ('VALIGN',(0,0),(0,-1),'TOP'),
                        ('ALIGN',(3,0),(3,-1), 'LEFT'),
                        ('FONTNAME', (6,0),(6,-1), 'Arialuni'),
                    ])

    Story.append(h)

    element = []
    tableheader = ['No.','Image', 'Product  Description', 'Quantity' ,'Price']
    #tableheader = ['No.','Image', 'Product      Description                                                            ', 'Quantity' ,'Price']

    element.append(tableheader)
    loopcounter = 1
    grund_total = 0
    for item in course.orderitem_set.all():

        myitem = []
        myitem.append( loopcounter )
        img = settings.MEDIA_ROOT+"/" +str(item.product.image.url).split("/")[2]
        I = Image(img)
        I.drawHeight = 0.85*inch
        I.drawWidth = 0.85*inch

        myitem.append( I )
        productname = item.orderitem_name

        line_remark =""
        if item.is_special:
            special = "★ Customized Product"
            productname = "%s      %s" %(item.orderitem_name, special)

        if item.line_remark is not None:
            line_remark = "%s %s" %("Remark: ", item.line_remark)


        desctiption = "Watt: "+ str(item.orderitem_watt) + " , Option1:" + item.orderitem_option1 + " , Beam Angle:" + item.orderitem_beam_angle + ' , CRI: ' + str(item.orderitem_cri) + ' , CCT: ' +item.orderitem_cct
        myitem.append( productname + '\n' +desctiption + '\nDimming Option:'+ str(item.orderitem_dimming) + '\nModel No: '+ item.orderitem_modelname + '\n' + line_remark )

        qty_group = [  item.quantity, item.quantity1, item.quantity2, item.quantity3]
        price_group = [item.price, item.price1, item.price2, item.price3]

        str_qty = ''
        str_price = ''

        for q in qty_group:
            if q is not None:
                str_qty += str('{:,.0f}'.format(int(q)))+'\n'

        for p in price_group:
            if p is not None:
                str_price += str('${:,.2f}'.format(float(p)))+'\n'


        myitem.append( str_qty )
        myitem.append( str_price )

        element.append(myitem)
        loopcounter += 1

    #repeatRows=1 是指第一行(表頭) 換頁時會重複
    t = Table(element, colWidths=[0.3*inch, 1.0*inch, 4.6*inch,  0.8*inch, 1.0*inch] , repeatRows=1)

    t.setStyle(
        TableStyle(
            [('BACKGROUND',(0,0),(4,0),colors.skyblue),
             ('ALIGN',(0,0),(3,0),'CENTER'),
             ('SIZE',(0,1),(0,-1), 8),
             ('SIZE',(2,1),(2,-1), 8),
             ('VALIGN',(0,0),(4,-1),'TOP'),
             ('ALIGN',(3,0),(4,-1), 'RIGHT'),
             ('TEXTCOLOR',(3,1),(4,-1), colors.blue),
             ('SIZE',(3,1),(4,-1), 8),
             ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
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

    #頁首的資訊
    #因為要套用字型Arialuni, 所以將comment改為Paragraph
    comment = Paragraph('''
       <para align=left spaceb=3><font face="Arialuni" >'''+ str(course.comment).replace('\n','<br/>\n') +'''</font></para>''',
       styles["BodyText"])
    footer = [['Remark:'],
                [ comment ],

              ]

    f = Table(footer)

    Story.append(f)


    style = getSampleStyleSheet()['Normal']
    style.leading = 8
    # generalterm.content   通用條款 Start
    #Story.append(PageBreak())
    # 因為要套用字型Arialuni, 所以將comment改為Paragraph
    terms = Paragraph('''
       <para align=left spaceb=3><fontSize=10 color=skyblue><strong>General Term and Conditions:</strong></fontSize><br/><font size="6">'''+ str(course.generalterm).replace('\n','<br/>\n') +'''</font></para>''',
       style )

    Story.append( KeepTogether(terms) )


    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPage )



def gen_quote(request,id):
    response = HttpResponse(content_type='application/pdf')
    filename = '-outline.pdf'
    response['Content-Disposition'] = 'filename=' + filename
    course = get_object_or_404(Order,id=id)
    _generate_pdf(course, response)

    return response







# 明確數量的報價單,有金額小計及總金額的報表模板
# 正式Quote-B
def _generate_pdfv2(course, output):
    from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table , TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle,PropertySet
    from reportlab.lib.units import mm, inch
    from reportlab.lib import colors
    from reportlab.platypus import XPreformatted, Preformatted
    from django.conf import settings
    from reportlab.pdfgen import canvas
    pdfmetrics.registerFont(TTFont('simhei', 'simhei.ttf'))
    pdfmetrics.registerFont(TTFont('Arialuni', 'arialuni.ttf'))


    #from cStringIO import StringIO

    doc = SimpleDocTemplate(output,pagesize=A4,
    rightMargin=.5*inch,leftMargin=.5*inch,
    topMargin=inch,bottomMargin=.6*inch)


    Story = [Spacer(1, 3.5*inch)]
    style = styles["Normal"]
    styleN = styles['Normal']
    styleH = styles['Heading1']

    ###
    stylesheet=getSampleStyleSheet()
    normalStyle = stylesheet['Normal']

    #頁首的資訊
    headerface = [['Quotation No',':', course.order_number],
              ['Customer',':', course.customer.title],
              ['Contact Person',':', course.contact.name],
              ['Contact Email',':', course.contact.email],
              ['Date',':', course.ord_date],
              ['Expired Date',':', course.effective_date],
              ]

    h = Table(headerface,style=[
                            ('ALIGN',(0,0),(0,-1), 'LEFT'),
                            ('FONTNAME', (2,0),(2,-1), 'Arialuni'),
                            ('SPAN',(1,-1),(1,-1)),
                            ('VALIGN',(0,0),(0,-1),'TOP'),
                        ])

    Story.append(h)
    Story.append(PageBreak())

    #因為要套用字型Arialuni, 所以將comment改為Paragraph
    comment = Paragraph('''
       <para align=left spaceb=3><font face="Arialuni">'''+ course.comment +'''</font></para>''',
       styles["BodyText"])



    #頁首的資訊
    header = [
              ['Quotation No',':', course.order_number,'','Date',':', course.ord_date],
              ['Customer',':', course.customer.title,'','Expired Date',':', course.effective_date],
              ['Contact Person',':', course.contact.name, '','Sales Contact',':', course.quote_user],
              ['Contact Email',':', course.contact.email,'', 'Email',':', course.quote_user.email],
              ['Payment Term',':', course.paymentterm,'','Currency',':' , course.currency],
              ['Price Term',':', course.priceterm,''],
              ]

    h = Table(header, colWidths=[1.0*inch, 0.1*inch, 2.8*inch, 0.3*inch, 0.9*inch, 0.1*inch, 2.0*inch] ,style=[
                        #('ALIGN',(0,0),(0,-1), 'LEFT'),
                        ('SPAN',(2,0),(3,0)),
                        ('FONTNAME', (2,0),(2,-1), 'Arialuni'),

                        ('VALIGN',(0,0),(0,-1),'TOP'),
                        ('ALIGN',(3,0),(3,-1), 'LEFT'),
                        ('FONTNAME', (6,0),(6,-1), 'Arialuni'),
                    ])

    Story.append(h)

    element = []
    #tableheader = ['No.','Image', 'Product / Description /  Dimming Option / Model Name                             ', 'Quantity' ,'Price', 'Amount']
    tableheader = ['No.', 'Product Description', 'Quantity' ,'Price', 'Sub-Total']

    element.append(tableheader)
    loopcounter = 1
    qty_amount = 0
    grund_total = 0
    for item in course.orderitem_set.all():

        myitem = []
        myitem.append( loopcounter )
        # img = settings.MEDIA_ROOT+"/" +str(item.orderitem_image.url).split("/")[2]
        # I = Image(img)
        # I.drawHeight = 0.85*inch
        # I.drawWidth = 0.85*inch

        productname = item.orderitem_name

        line_remark =""
        if item.is_special:
            special = "★ Customized Product"
            productname = "%s      %s" %(item.orderitem_name, special)

        if item.line_remark is not None:
            line_remark = "%s %s" %("Remark: ", item.line_remark)


        #myitem.append( I )
        desctiption = "Watt: "+ str(item.orderitem_watt) + " , Option1:" + item.orderitem_option1 + " , Beam Angle:" + item.orderitem_beam_angle + ' , CRI: ' + str(item.orderitem_cri) + ' , CCT: ' +item.orderitem_cct
        myitem.append( productname + '\n' +desctiption + '\nDimming Option:'+ str(item.orderitem_dimming) + '\nModel No: '+ item.orderitem_modelname + '\n' + line_remark )

        qty_group = [item.quantity]
        price_group = [item.price]
        #行小計
        sub_amount = item.quantity * item.price

        #金額總計
        qty_amount += item.quantity
        grund_total += sub_amount
        #print( '${:,.2f}'.format(qty_amount) )


        str_qty = ''
        str_price = ''

        for q in qty_group:
            if q is not None:
                str_qty += str( '{:,.0f}'.format(int(q)) )+'\n'

        for p in price_group:
            if p is not None:
                str_price += str( '${:,.2f}'.format(float(p)) )+'\n'


        myitem.append(  str_qty   )
        myitem.append(  str_price  )
        myitem.append( '${:,.2f}'.format(sub_amount)  )

        element.append(myitem)
        loopcounter += 1

    #repeatRows=1 是指第一行(表頭) 換頁時會重複
    t = Table(element, colWidths=[0.4*inch, 4.9*inch, 0.5*inch, 0.8*inch,  1.1*inch], repeatRows=1)

    t.setStyle(
        TableStyle(
            [('BACKGROUND',(0,0),(4,0),colors.skyblue),
             ('ALIGN',(0,0),(3,0),'CENTER'),
             ('SIZE',(0,1),(4,-1), 7),

             ('VALIGN',(0,0),(4,-1),'TOP'),
             ('ALIGN',(2,0),(4,-1), 'DECIMAL'),
             ('TEXTCOLOR',(4,1),(4,-1), colors.blue),
             ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
             ]
        )
    )

    Story.append(t)

    #頁首的資訊
    #因為要套用字型Arialuni, 所以將comment改為Paragraph
    comment = Paragraph('''
       <para align=left spaceb=3><font face="Arialuni">'''+ str(course.comment).replace('\n','<br/>\n') +'''</font></para>''',
       styles["BodyText"])
    footer = [  ['', '', '', '', ' ' ,'Quantity Total:', '{:,.0f}'.format(qty_amount) ],
                ['', '', '', '', ' ' ,'Grand Total:',  '${:,.2f}'.format(grund_total)  ],
                ['','', '', '', '', ' ',''],
                [ 'Remark:',comment ],
              ]

    f = Table(footer,style=[
                            ('ALIGN',(0,0),(6,-1), 'RIGHT'),
                            #('ALIGN',(0,0),(0,-1), 'LEFT'),
                            ('FONTNAME', (0,0),(0,-1), 'Arialuni'),
                            ('VALIGN',(0,0),(0,-1), 'TOP'),
                            ('SPAN',(1,3),(6,-1)),
                        ])

    Story.append(f)







    style = getSampleStyleSheet()['Normal']
    style.leading = 8
    # generalterm.content   通用條款 Start
    #Story.append(PageBreak())
    # 因為要套用字型Arialuni, 所以將comment改為Paragraph
    terms = Paragraph('''
       <para align=left spaceb=3><fontSize=10 color=skyblue><strong>General Term and Conditions:</strong></fontSize><br/><font size="6">'''+ str(course.generalterm).replace('\n','<br/>\n') +'''</font></para>''',
       style )

    Story.append( KeepTogether(terms) )

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPage )


# 明確數量的報價單,有金額小計及總金額的
@login_required
def gen_pdfv2(request,id):
    response = HttpResponse(content_type='application/pdf')
    filename = 'Quotation.pdf'
    response['Content-Disposition'] = 'filename=' + filename
    course = get_object_or_404(Order,id=id)
    _generate_pdfv2(course, response)

    return response




#參考的操作範例, 已不使用
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





def order_print(request, id):

    order = get_object_or_404(Order,id=id)
    html = render_to_string('quoted/order_print.html',{'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\"order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html, base_url = request.build_absolute_uri() ).write_pdf(response,stylesheets=[weasyprint.CSS( settings.STATIC_ROOT + '/css/pdf.css')])

    return response
