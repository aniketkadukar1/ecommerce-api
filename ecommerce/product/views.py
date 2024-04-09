from rest_framework import viewsets
from .models import Category, Brand, Product, ProductLine
from . serializers import CategorySerializer, BrandSerializer, ProductSerializer, ProductLineSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.db.models import Prefetch



class CategoryViewSet(viewsets.ViewSet):
    """
    Simple Viewset for viewing categories
    """
    queryset = Category.objects.all().isactive()
    
    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """
    Simple Viewset for viewing brands
    """
    queryset = Brand.objects.all().isactive()
    
    
    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)
    

class ProductViewSet(viewsets.ViewSet):
    """
    Simple Viewset for viewing products
    """
    queryset = Product.objects.all().isactive()


    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(self.queryset.filter(slug=slug).select_related("category", "brand").prefetch_related(Prefetch("product_line")).prefetch_related(Prefetch("product_line__product_image")), many=True)
        return Response(serializer.data)
         
    
    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=["get"], detail=False, url_path=r"category/(?P<category>\w+)/all",url_name="all" )
    def list_product_by_category(self, request, category=None):
        """
        An endpoint to return product by category
        """
        serializer = ProductSerializer(self.queryset.filter(category__name=category), many=True)
        return Response(serializer.data)
    


class ProductLineViewSet(viewsets.ViewSet):
    """
    Simple Viewset for viewing product line
    """
    queryset = ProductLine.objects.all().isactive()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductLineSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    

