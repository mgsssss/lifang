from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Order(models.Model):
    choices = ( ('대기중', '대기중' ), ('결제대기', '결제대기중' ), ('결제완료', '결제완료' ), ('환불', '환불' ),)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자' )
    main_img = models.CharField(max_length=256, verbose_name='대표이미지', null=True,default='')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name='상품명' )
    category1 = models.CharField(max_length=256, verbose_name='카테고리1', null=True,default='')
    category2 = models.CharField(max_length=256, verbose_name='카테고리2', null=True,default='')
    nation = models.CharField(max_length=256, verbose_name='국가', null=True,default='')
    channel = models.CharField(max_length=256, verbose_name='유통채널', null=True,default='')
    product_price = models.CharField(max_length=256, verbose_name='가격', null=True,default='')
    vendor_name = models.CharField(max_length=256, verbose_name='판매상명', null=True,default='')
    crackdown = models.CharField(max_length=256, verbose_name='단속근거', null=True,default='')
    prejudice1 = models.CharField(max_length=256, verbose_name='침해유형1', null=True,default='')
    prejudice2 = models.CharField(max_length=256, verbose_name='침해유형2', null=True,default='')
    report_date = models.CharField(max_length=256, verbose_name='신고일자', null=True,default='')
    report_result = models.CharField(max_length=256, verbose_name='신고결과', null=True,default='')
    url = models.CharField(max_length=256, verbose_name='상품URL', null=True,default='')
    etc = models.CharField(max_length=256, verbose_name='비고', null=True,default='')
    quantity = models.IntegerField(verbose_name='수량')
    status = models.CharField(
        choices=choices,  default='대기중', max_length=32, verbose_name='상태'
    )
    memo = models.TextField(null=True, blank = True, verbose_name='메모')
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.lifanguser) + ' ' + str(self.product)
   
    class Meta:
        db_table = 'order'
        verbose_name = '프로젝트'
        verbose_name_plural = '프로젝트'
        
    