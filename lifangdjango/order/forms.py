from django import forms 
from .models import Order
from product.models import Product
from django.db import transaction

class RegisterForm(forms.Form):
    
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
                 
                 
    quantity = forms.IntegerField(
        error_messages={'required' : '수량을 입력해주세요.'},
        label="수량")
   
        
    product = forms.CharField(error_messages={'required' : '상품명을 입력해주세요'},
                               label="상품설명", widget=forms.HiddenInput)
    
    
    
    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
          
        if not (quantity and product and lifanguser):
        
            self.add_error('product', '값이 없습니다.')
            self.add_error('lifanguser', '값이 없습니다.')
                    
      
        
        # name = cleaned_data.get('name')
        # price = cleaned_data.get('price')
        # decription = cleaned_data.get('decription')
        # stock = cleaned_data.get('stock')
        
        # if name and price and decription and stock:
            
        #     product=Product(
        #         name=name,
        #         price=price,
        #         decription=decription,
        #         stock=stock
        #     )
        #     product.save()