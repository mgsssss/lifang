import datetime
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.db import transaction
from django.urls import path
from .models import Order

#태그를 바로 쓰면 안된다. 아래 함수를 쓰면 html로 인식한다.
from django.utils.html import format_html

# Register your models here.

def refund(ModelAdmin, request, queryset):
    
    # if obj.status == '환불' : continue
    # 쿼리셋의 응용으로 수량 제거
   
    
    with transaction.atomic(): 
        qs = queryset.filter(~Q(status='환불'))
        ct = ContentType.objects.get_for_id(queryset.model)
        for obj in qs: 
            obj.product.stock += obj.quantity
            obj.product.save()
            
            LogEntry.objects.log_action(
                user_id = request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr='주문 환불',
                action_flag=CHANGE,
                change_message='주문 발행'
 
                
            )
        
            qs.update(status='환불')
    
refund.short_description = '환불'    

class OrderAdmin(admin.ModelAdmin):
    
    list_filter = ('status',)
    list_display = ('main_img', 'product', 'category1', 'category2', 'nation', 'channel', 'product_price', 'vendor_name', 'crackdown', 'prejudice1', 'prejudice2', 'report_date', 'report_result',  'url', 'etc', )
    change_list_template = 'admin/order_change_list.html'
    change_form_template = 'admin/order_change_form.html'
    
    actions = [ refund ]
    
    def action(self,obj):
        
        if obj.status != '환불' :
            return format_html(f'<input type= "button" value="환불" onclick="order_refund_submit({obj.id})" class="btn btn-primary btn-sm">')
            
    
    def styled_status(self,obj):
        
        if obj.status == '환불':
            return format_html(f'<span style="color:red">{obj.status}</span>') #obj.status
        elif obj.status == '결제완료':
            return format_html(f'<span style="color:green">{obj.status}</span>') #obj.status
        
        return obj.status
    

    def changelist_view(self, request, extra_context=None):
    # 우리가 원하는 동작
        extra_context = { 'title' : '주문 목록' }
        
        if request.method == 'POST':
            
                obj_id = request.POST.get('obj_id')
                
                if obj_id:
                    qs = Order.objects.filter(pk=obj_id)
                    ct = ContentType.objects.get_for_model(qs.model)
                    for obj in qs: 
                        obj.product.stock += obj.quantity
                        obj.product.save()
                        
                        LogEntry.objects.log_action(
                            user_id = request.user.id,
                            content_type_id=ct.pk,
                            object_id=obj.pk,
                            object_repr='주문 환불',
                            action_flag=CHANGE,
                            change_message='주문 발행')

                    qs.update(status='환불')
                
        return super().changelist_view(request, extra_context)
    
    
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    # 우리가 원하는 동작
        #order = Order.objects.get(pk=object_id)
        #extra_context = { 'title' : f'{order.lifanguser.email}의 {order.product.name} 주문 수정하기' }
        #extra_context['show_save_and_add_another'] = False
        #extra_context['show_save_and_continue'] = False
        extra_context = []
        return super().changeform_view(request, object_id, form_url, extra_context)
            
    
    def get_urls(self):
        urls = super().get_urls()
        date_urls = [
            
            path('date_view/', self.date_view),
        ]
        
        return date_urls + urls
    
    
    def date_view(self, request):
        week_date = datetime.datetime.now() - datetime.timedelta(days=7)
        week_data = Order.objects.filter(registered_dttm__gte=week_date)
        data =  Order.objects.filter(registered_dttm__lte=week_date)
        context = dict(
            self.admin_site.each_context(request),
            week_data = week_data,
            data = data)
        return TemplateResponse(request, 'admin/order_date_view.html', context)
        
    styled_status.short_description = '상태'
    

admin.site.register(Order, OrderAdmin)