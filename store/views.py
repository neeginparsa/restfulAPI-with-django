
from typing import Counter
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import api_view
from django.db.models.aggregates import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet,ModelViewSet #use for related viewclass in singleclass
from rest_framework import status
from store.filter import ProductFilter
from .models import Collection, OrderItem, Product, Review, Cart
from .serializers import CartSerializer, ProductSerializer, ReviewSerializer,collectionserializer
from store import serializers

class productViewSet(ModelViewSet): #readonlyModelViewSet--> just read and cant be able to update, delete or...
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination  ---> for just pagination products
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price','last_update']
    
    
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


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])#filter baraye inke review ha be hame product ha ekhtesas dade nashe(har product ba id be review motasel)
     
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
class CartViewSet(CreateModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    