from typing import Counter
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from django.db.models.aggregates import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet #use for related viewclass in singleclass
from rest_framework import status
from .models import Collection, OrderItem, Product
from .serializers import ProductSerializer,collectionserializer
from store import serializers

class productViewSet(ModelViewSet): #readonlyModelViewSet--> just read and cant be able to update, delete or...
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_contex(self):
        return {'request': self.request}

    def destroy(request,*args ,**kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() >0:
            return Response({'error':'product cannot be deleted '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request,*args ,**kwargs)


class collectionViewSet(ModelViewSet):
    queryset= Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = collectionserializer
    def delete(self,request,pk):
        collection= get_object_or_404 (Collection,pk=pk)
        if collection.products.count() >0:
            return Response({'error':'collection cannot be deleted '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



