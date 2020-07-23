import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import *
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def export_to_csv(modeladmin,request,queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content_Disposition'] ="attachment;filename={}.csv".format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [filed for filed in opts.get_fields() if not filed.many_to_many and not filed.one_to_many]
    writer.writerow(field.verbose_name for field in fields)

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj,field)
            if isinstance(value,datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = '导出csv格式'


def order_detail(obj):
    return mark_safe('<a href="{}">视图</a>'.format(reverse('orders:admin_order_detail',args=(obj.id,))))
order_detail.short_description = '订单详情'

def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf',args=(obj.id))))
order_pdf.short_description = '发票'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = [export_to_csv]
    list_display = ['id','first_name','last_name','email','address','postal_code','city','paid','created','updated',order_detail,order_pdf]
    list_filter = ['paid','created','updated']
    inlines = [OrderItemInline]


