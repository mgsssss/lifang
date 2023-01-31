from django.shortcuts import render, redirect
from django.views.generic.edit import FormView 
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password
from .models import Lifanguser, Company
from product.models import Product, Project

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import CompanySerializer

from django.views.generic import TemplateView
from django.db.models import F, Sum, Count, Case, When
from product.category import product_category, type_choices
# Create your views here.

# 사이트별(완), 침해유형별, 카테고리별(완) <- 기업침해 기업별로 다 보여주는것

# 사이트별(완), 침해유형별, 카테고리별 <- 프로젝트 침해 프로젝트 별로 다 보여주는것


class ProjectTypeChartTemplateView(TemplateView):
    template_name = 'admin/chart/project_type.html'
    extra_context = {'title' : '프로젝트별 침해유형 차트', 'site_title':'리팡 관리자 화면', 'site_header':'리팡 관리자 화면'}
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        company_id = self.request.user.company.id
        project_id = kwargs.get('pk', None)
        if self.request.user.is_superuser == True:
            context['project'] = Project.objects.all().values('id', 'company__name', 'name')
        else:
            company_id = self.request.user.company.id
            context['project'] = Project.objects.filter(company__id = company_id).values('id', 'company__name', 'name')
        
        if project_id == None:
            query_set = Project.objects.filter(company=company_id).order_by('-id').values('id').first()
            project_id = query_set['id']
        context['project_id'] = int(project_id)
        
        cnt = Product.objects.filter(project=project_id).values('type_id').annotate(cnt=Count('type_id')).values('cnt', 'type_id')
        
        choices = type_choices()
        type_dict = {}
        for types in choices:
            for typ in types:
                for t in typ:
                    if type(t[0]) == int:
                        type_dict[t[0]] = t[1]
        for c in cnt:
            c['type_name'] = type_dict[c['type_id']]
        context['cnt'] = cnt
        return context

class ProjectCategoryChartTemplateView(TemplateView):
    template_name = 'admin/chart/project_category.html'
    extra_context = {'title' : '프로젝트별 침해유형 차트', 'site_title':'리팡 관리자 화면', 'site_header':'리팡 관리자 화면'}
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        company_id = self.request.user.company.id
        project_id = kwargs.get('pk', None)
        if self.request.user.is_superuser == True:
            context['project'] = Project.objects.all().values('id', 'company__name', 'name')
        else:
            company_id = self.request.user.company.id
            context['project'] = Project.objects.filter(company__id = company_id).values('id', 'company__name', 'name')
        
        if project_id == None:
            query_set = Project.objects.filter(company=company_id).order_by('-id').values('id').first()
            project_id = query_set['id']
        context['project_id'] = int(project_id)
        
        cnt = Product.objects.filter(project=project_id).values('category_id').annotate(cnt=Count('category_id')).values('cnt', 'category_id')
        choices = product_category()
        category_dict = {}
        for categorys in choices:
            for category in categorys:
                for c in category:
                    if type(c[0]) == int:
                        category_dict[c[0]] = c[1]
        for c in cnt:
            c['category_name'] = category_dict[c['category_id']]
        context['cnt'] = cnt        
        print(cnt)
        return context

class TypeChartTemplateView(TemplateView):
    template_name = 'admin/chart/type.html'
    extra_context = {'title' : '기업별 침해유형 차트', 'site_title':'리팡 관리자 화면', 'site_header':'리팡 관리자 화면'}
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        company_id = self.request.user.company.id
        #Project.objects.prefetch_related('product_set').values('product__site_name').annotate(site_cnt=Count('product__site_name'), product_name=F('project_id')).values('site_cnt', 'product_name')
        if self.request.user.is_superuser == True:
            company_id = kwargs.get('pk', 1)
            context['company'] = Company.objects.all().values('id', 'name')
            for company in context['company']:
                if company['id'] == int(company_id):
                    context['company_name'] = company['name']
        else:
            company_id = self.request.user.company.id
            context['company_name'] = self.request.user.company.name
        cnt = Product.objects.filter(project__company_id=company_id).values('type_id').annotate(cnt=Count('type_id')).values('cnt', 'type_id')
        
        choices = type_choices()
        type_dict = {}
        for types in choices:
            for typ in types:
                for t in typ:
                    if type(t[0]) == int:
                        type_dict[t[0]] = t[1]
        for c in cnt:
            c['type_name'] = type_dict[c['type_id']]
        context['cnt'] = cnt
        
        return context

class CompanyChartTemplateView(TemplateView):
    template_name = 'admin/chart/company.html'
    extra_context = {'title' : '기업별 침해유형 차트', 'site_title':'리팡 관리자 화면', 'site_header':'리팡 관리자 화면'}
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        company_id = self.request.user.company.id
        #Project.objects.prefetch_related('product_set').values('product__site_name').annotate(site_cnt=Count('product__site_name'), product_name=F('project_id')).values('site_cnt', 'product_name')
        if self.request.user.is_superuser == True:
            company_id = kwargs.get('pk', 1)
            context['company'] = Company.objects.all().values('id', 'name')
            for company in context['company']:
                if company['id'] == int(company_id):
                    context['company_name'] = company['name']
        else:
            company_id = self.request.user.company.id
            context['company_name'] = self.request.user.company.name
        cnt = Product.objects.filter(project__company_id=company_id).values('site_name').annotate(cnt=Count('site_name')).values('cnt', 'site_name')
        choices = {1:'타오바오', 2:'1688', 3:'알리바바', 4:'쇼피', 5: '기타'}
        for c in cnt:
            c['site'] = choices[c['site_name']]
        context['cnt'] = cnt
        return context
    
class ProjectChartTemplateView(TemplateView):
    template_name = 'admin/chart/project.html'
    extra_context = {'title' : '프로젝트별 침해유형 차트', 'site_title':'리팡 관리자 화면', 'site_header':'리팡 관리자 화면'}
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        company_id = self.request.user.company.id
        project_id = kwargs.get('pk', None)
        if self.request.user.is_superuser == True:
            context['project'] = Project.objects.all().values('id', 'company__name', 'name')
        else:
            company_id = self.request.user.company.id
            context['project'] = Project.objects.filter(company__id = company_id).values('id', 'company__name', 'name')
        
        if project_id == None:
            query_set = Project.objects.filter(company=company_id).order_by('-id').values('id').first()
            project_id = query_set['id']
        
        cnt = Product.objects.filter(project=project_id).values('site_name').annotate(cnt=Count('site_name')).values('cnt', 'site_name')
        choices = {1:'타오바오', 2:'1688', 3:'알리바바', 4:'쇼피', 5: '기타'}
        for c in cnt:
            c['site'] = choices[c['site_name']]        
        context['cnt'] = cnt
        context['project_id'] = int(project_id)
        
        return context
    
class CategoryChartTemplateView(TemplateView):
    template_name = 'admin/chart/category.html'
    extra_context = {'title' : '기업별 침해유형 차트', 'site_title':'리팡 관리자 화면', 'site_header':'리팡 관리자 화면'}
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        company_id = self.request.user.company.id
        #Project.objects.prefetch_related('product_set').values('product__site_name').annotate(site_cnt=Count('product__site_name'), product_name=F('project_id')).values('site_cnt', 'product_name')
        if self.request.user.is_superuser == True:
            company_id = kwargs.get('pk', 1)
            context['company'] = Company.objects.all().values('id', 'name')
            for company in context['company']:
                if company['id'] == int(company_id):
                    context['company_name'] = company['name']
        else:
            company_id = self.request.user.company.id
            context['company_name'] = self.request.user.company.name
        cnt = Product.objects.filter(project__company_id=company_id).values('category_id').annotate(cnt=Count('category_id')).values('cnt', 'category_id')
        choices = product_category()
        category_dict = {}
        for categorys in choices:
            for category in categorys:
                for c in category:
                    if type(c[0]) == int:
                        category_dict[c[0]] = c[1]
        for c in cnt:
            c['category_name'] = category_dict[c['category_id']]
        context['cnt'] = cnt
        return context
    

class CompanyAPIView(APIView):
    def get(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)
        return Response(serializer.data)
    

def index(request):
    return render(request, 'index.html', {'email': request.session.get('user')})


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'
    
    #유효성 검사
    def form_valid(self, form):
        lifanguser = Lifanguser(
            email=form.data.get('email'),
            password=make_password(form.data.get('password')),
            level='user'
        )
        lifanguser.save()
        
        return super().form_valid(form)
    
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'
    
    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        
        return super().form_valid(form)
    

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
        
    return redirect('/')



# {% for project in projects %}
#   {{ project.name }}
#     {% for product in project.product_set.all %}
#         {{product.get_site_name_display }}
#       <!-- no entries -->
#     {% endfor %}
# {% endfor %}
