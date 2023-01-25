from django.contrib import admin
from .models import *
from product.models import Product

# Register your models here.

class LifanguserAdmin(admin.ModelAdmin):
    list_display = ('email', )
    
    def changelist_view(self, request, extra_context=None):
        # 우리가 원하는 동작
        extra_context = { 'title' : '사용자 목록' }
        
        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    # 우리가 원하는 동작
        #product = Product.objects.get(pk=object_id)
        
        extra_context = { 'title' : f'{Lifanguser.email} 수정하기' }
        return super().changeform_view(request, object_id, form_url, extra_context)
            

admin.site.register(Company)    
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Lifanguser, LifanguserAdmin)

admin.site.site_header = '리팡어드민'
admin.site.index_title = '리팡어드민'
admin.site.site_title = '리팡어드민'
