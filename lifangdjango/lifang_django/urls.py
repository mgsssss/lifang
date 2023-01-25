"""lifang_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import datetime
from django.contrib import admin
from django.template.response import TemplateResponse

from django.urls import path, include, re_path
from lifanguser.views import index, logout, RegisterView, LoginView
from product.views import (ProductList, ProductCreate, ProductDetail,
     ProductListAPI, ProductDetailAPI, ProductAPIView)
from order.views import OrderCreate, OrderList
from django.views.generic import TemplateView

from order.models import Order
from .functions import get_exchange

from django.conf import settings
from django.conf.urls.static import static

origin_index = admin.site.index

#함수를 만들어서 원하는 정보를 중간에 끼워놈
def lifang_admin_index(request, extra_context=None):
    
    base_date = datetime.datetime.now() - datetime.timedelta(days=7)
    order_data = {}
    for i in range(7):
        target_dttm = base_date + datetime.timedelta(days=i)
        date_key = target_dttm.strftime('%Y-%m-%d')
        taget_date = datetime.date(target_dttm.year, target_dttm.month, target_dttm.day)
        order_cnt = Order.objects.filter(registered_dttm__date=taget_date).count()
        order_data[date_key] = order_cnt
        
    extra_context = {
        'orders' : order_data,
        #'exchange' : get_exchange()
    }
    
    
    return origin_index(request, extra_context)

admin.site.index = lifang_admin_index
    
    
urlpatterns = [
    
    #re_path 정확히 일치하는 애만 연결
    re_path(r'^admin/manual/$', TemplateView.as_view(template_name='admin/manual.html', 
            extra_context={'title' : '매뉴얼', 'site_title':'리팡 관리자 화면', 'site_header':'리팡 관리자 화면'})),
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('', index),
    path('logout/',logout),
    path('register/', RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('product/', ProductList.as_view()),
    path('product/<int:pk>', ProductDetail.as_view()),    
    path('product/create/', ProductCreate.as_view()),
    path('order/create/', OrderCreate.as_view()),
    path('order/', OrderList.as_view()),
    
    path('api/product/',ProductListAPI.as_view()),
    path('api/product/<int:pk>',ProductDetailAPI.as_view()),
    
    path('api/product_apiview/',ProductAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
