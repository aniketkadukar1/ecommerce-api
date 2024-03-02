from rest_framework import viewsets
from .models import Category
from . serializers import CategorySerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

class CategoryViewSet(viewsets.ViewSet):
    """
    Simple Viewset for viewing categories
    """
    queryset = Category.objects.all()
    
    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


