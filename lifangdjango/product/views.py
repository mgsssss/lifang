from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.http import Http404

from .models import Product, Project

from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from lifanguser.decorator import login_requierd, admin_requierd
from .forms import RegisterForm 
from .serializer import ProductSerializer, ProjectSerializer

from order.forms import RegisterForm as OrderForm 
from django.http import JsonResponse
# class ProjectDetailAPIView(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             raise Http404

#     def put(self, request, pk, format=None):
#         project = self.get_object(pk)
#         serializer = ProjectSerializer(project, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def ProjectDetailAPIView(request, pk):
    if request.method == "GET":
        cnt = Product.objects.filter(project_id=pk).count()
        project = Project.objects.get(id=pk)
        project.fake_num = cnt
        project.save()
        
        return JsonResponse({"cnt": project.fake_num})

class ProjectAPIView(APIView):
    def get(self, request):
        products = Project.objects.all()
        serializer = ProjectSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
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