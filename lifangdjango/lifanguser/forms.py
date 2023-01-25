from django import forms 
from .models import Lifanguser
from django.contrib.auth.hashers import check_password


class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={'required' : '아이디를 입력해주세요.'},
        max_length=64, label="이메일")
   
    password = forms.CharField(error_messages={'required' : '비밀번호를 입력해주세요.'},
                               widget=forms.PasswordInput, label="비밀번호")
    
    re_password = forms.CharField(error_messages={'required' : '비밀번호를 입력해주세요.'},
                               widget=forms.PasswordInput, label="비밀번호 확인")
    
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        
        if password and re_password:
           if password != re_password:
               self.add_error('password', '비밀번호가 서로 다릅니다.')
               self.add_error('re_password', '비밀번호가 서로 다릅니다.')

               
               
class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={'required' : '아이디를 입력해주세요.'},
        max_length=64, label="이메일")
   
    password = forms.CharField(error_messages={'required' : '비밀번호를 입력해주세요.'},
                               widget=forms.PasswordInput, label="비밀번호")
    

    #유효성 검사하는 부분과 모델의 분리는 리팩토링

    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email and password:
            
            #예외처리는 try로 함
            
            try:
                lifanguser = Lifanguser.objects.get(email=email)
            except lifanguser.DoesNotExist:
                self.add_error('email', '이메일이 없습니다.')
                return
                       
            
            if not check_password(password, lifanguser.password):
                self.add_error('password','비밀번호가 틀렸습니다.')
