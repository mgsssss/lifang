from django.db import models
from lifanguser.models import *
from .category import product_category

# 유저 -> 컴퍼니 -> 프로젝트 -> 프로덕트 -> 카테고리
                    # -> 브랜드 사이트 이름 

# 프로젝트
class Project(models.Model):
    choices = ((1, '타오바오'), (2, '1688'), (3, '알리바바'), (4, '쇼피'),)
    # 타오바오 1688 라자다 알리바바 쇼피
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    fake_num = models.IntegerField(verbose_name='가품발견수')
    site_name = models.SmallIntegerField('사이트 이름', choices=choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'project'

# 상품
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    # image = models.ImageField(max_length=255, upload_to='images/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category_id = models.SmallIntegerField(choices=product_category(), default=1)
    brand_name = models.CharField(max_length=256, verbose_name='브랜드명', null=True, default='')
    name = models.CharField(max_length=256, verbose_name='상품명', null=True,default='')
    price = models.IntegerField(verbose_name='상품가격')
    url = models.URLField(max_length=255)
    # descrtiption = models.TextField(verbose_name='상품설명')
    created_at = models.DateTimeField(auto_now_add=True) # 등록날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정날짜
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'product'
        verbose_name = '상품'
        verbose_name_plural = '상품'
        













