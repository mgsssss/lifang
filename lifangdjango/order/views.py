from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from .forms import RegisterForm
from .models import Order

# Create your views here.


class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'
    
    def form_invaild(self, form):
        return redirect('/prodect/' + form.product)
    
    def get_form_kwargs(self, **kwangs):
        kw = super().get_form_kwargs(**kwangs)
        kw.update({
            'request' : self.request
            
            
        })
        return kw
    
class OrderList(ListView):
    template_name = 'order.html'
    context_object_name = 'order_list'
    
    def get_queryset(self, **kwargs) :
        queryset = Order.objects.filter(lifanguser__email=self.request.session.get('user'))
        return queryset