#로그인을 안한 상태에서 로그인을 하면 로그인 페이지로 이동 시키는 것
from django.shortcuts import redirect
from .models import Lifanguser

def login_requierd(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        
        if user is None or not user:
            return redirect('/login')
        
        return function(request, *args, **kwargs)
    
    return wrap

def admin_requierd(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        
        if user is None or not user:
            return redirect('/login')
        
        user == Lifanguser.objects.get(email=user)
        if user.level != 'admin':
            return redirect('/')
        
        return function(request, *args, **kwargs)
    
    return wrap