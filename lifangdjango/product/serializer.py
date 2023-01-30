from rest_framework import serializers
from .models import Product, Project

class ProductSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(use_url=True)
    class Meta:
        model = Product
        fields = '__all__'
        
        
class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ('id', 'company', 'name', 'fake_num')
        
