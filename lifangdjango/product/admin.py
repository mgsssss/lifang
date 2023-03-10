from django.contrib import admin
from .models import Product, Project
from lifanguser.models import Company
from django.contrib.humanize.templatetags.humanize import intcomma

#태그를 바로 쓰면 안된다. 아래 함수를 쓰면 html로 인식한다.
from django.utils.html import format_html

class ProductInline(admin.StackedInline):
    model = Product
    extra = 0
    
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'fake_num', 'created_at']
    search_fields = ['name']
    inlines = [ProductInline]
    
    def get_queryset(self, obj):
        qs = super(ProjectAdmin, self).get_queryset(obj)
        if obj.user.is_superuser == False:
            company = Company.objects.get(user_id=obj.user.id)
            qs = qs.filter(company=company.id)
        return qs

class ProductAdmin(admin.ModelAdmin):
    # 'project__company_name', 
    list_display = ('brand_name', 'name', 'price', 'category_id' ,'type_id', 'site_name', 'created_at')
    list_filter = ('project__name',)
    search_fields = ['name', 'project__name']

    
    def get_queryset(self, obj):
        qs = super(ProductAdmin, self).get_queryset(obj)
        if obj.user.is_superuser == False:
            company = Company.objects.get(user_id=obj.user.id)
            qs = qs.filter(project__company=company.id)
        return qs        
    
    def price_format(self,obj):
      price = intcomma(obj.price)
      return f'{price}원'

    
    
    # def styled_stock(self,obj):
        
    #     stock = obj.stock
        
    #     if stock <= 50:
    #         stock = intcomma(stock)
    #         return format_html(f'<b><span style="color:red">{stock}개</span></b>') 
    #     return f'{intcomma(stock)}개'
    
    def changelist_view(self, request, extra_context=None):
    # 우리가 원하는 동작
        extra_context = { 'title' : '상품 목록' }
        return super().changelist_view(request, extra_context)
    
    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    # # 우리가 원하는 동작
    #     product = Product.objects.get(pk=object_id)
        
    #     extra_context = { 'title' : f'{product.name} 수정하기' }
    #     return super().changeform_view(request, object_id, form_url, extra_context)

            
    
    #price_format.short_description = '가격'
    #styled_stock.short_description = '발견한 가품수'
admin.site.register(Product, ProductAdmin)
admin.site.register(Project, ProjectAdmin)