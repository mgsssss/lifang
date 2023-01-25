from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='회사명')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name    
    
    class Meta:
        db_table = 'company'
        verbose_name = '회사명'
        verbose_name_plural = '회사명'


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
        
    class Meta:
        db_table = 'category'
        
        
class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'sub_category'


class Lifanguser(models.Model):
    email = models.EmailField(max_length=128, verbose_name='사용자 이메일')
    password = models.CharField(max_length=128, verbose_name='비밀번호')
    level = models.CharField(max_length=64, verbose_name='등급', choices={('admin', 'admin'), ('user', 'user'),})
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'