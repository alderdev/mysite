from django.contrib import admin

from .models import WorkOrder, ZmmsOption, MaterialCtrlOption, OrderCategory

# Register your models here.

class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ( 'category', 'work_order', 'zmms', 'material_ctrl', 'recevice_date', 'ships_order', 'reuqest_user','product',  'ord_amount', 'deliverly' ,'manage_memo')
    search_fields = ['work_order','ships_order','reuqest_user']
    list_display_links = ('work_order',)
    list_per_page = 10



admin.site.register(ZmmsOption)
admin.site.register(MaterialCtrlOption)
admin.site.register(OrderCategory)
admin.site.register(WorkOrder, WorkOrderAdmin)
