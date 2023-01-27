from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.http import Http404

from .models import Product

from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from lifanguser.decorator import login_requierd, admin_requierd
from .forms import RegisterForm 
from .serializer import ProductSerializer

from order.forms import RegisterForm as OrderForm 


class ProductAPIView(APIView):
    
    def get(self, request):
        # products = Product.objects.filter(active=True)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#레스트 프레임워크
class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        print(self.request.user.id)
        return Product.objects.all().order_by('id')
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
#레스트 프레임워크
class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.all().order_by('id')
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    

class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'

@method_decorator(admin_requierd, name='dispatch')
class ProductCreate(FormView):
    model = Product
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'
    

class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data( **kwargs)
        context['form'] = OrderForm(self.request)
        return context