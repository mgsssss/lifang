from django import forms 
from .models import Product

class RegisterForm(forms.Form):
    name = forms.CharField(
        error_messages={'required' : '상품명을 입력해주세요.'},
        max_length=64, label="상품명")
   
    price = forms.IntegerField(error_messages={'required' : '상품가격을 입력해주세요.'},
                               label="상품가격")
    
    decription = forms.CharField(error_messages={'required' : '상품명을 입력해주세요'},
                               label="상품설명")
    
    stock = forms.IntegerField(error_messages={'required' : '재고를 입력해주세요.'},
                               label="재고")
    
    
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        decription = cleaned_data.get('decription')
        stock = cleaned_data.get('stock')
        
        if name and price and decription and stock:
            
            product=Product(
                name=name,
                price=price,
                decription=decription,
                stock=stock
            )
            product.save()