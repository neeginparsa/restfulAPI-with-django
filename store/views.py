from typing import Counter
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from django.db.models.aggregates import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Collection, Product
from .serializers import ProductSerializer,collectionserializer
from store import serializers

class ProductList(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related('collection').all()
    def get_serializer_class(self):
        return ProductSerializer
    def get_serializer_contex(self):
        return {'request': self.request}
    #...............insted.....................
    
    # def get(self,request):
    #     querySet= Product.objects.select_related('collection').all() #select_related--> baraye farakhani fieldi az classe digar
    #     serializer= ProductSerializer(querySet,many=True)
    #     return Response(serializer.data)
    # def post(self,request):
    #     serializer= ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class collectionlist(ListCreateAPIView):
    def get_queryset(self):
        return Collection.objects.annotate(products_count=Count('products')).all()
    def get_serializer_class(self):
        return collectionserializer
    #...............insted.....................
    # def get(self,request):
    #     querySet= Collection.objects.annotate(products_count=Count('products')).all() 
    #     serializer= collectionserializer(querySet,many=True)
    #     return Response(serializer.data)
    # def post(self,request):
    #     serializer= collectionserializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)



class collectionDetail(RetrieveUpdateDestroyAPIView):
    queryset= Collection.objects.annotate(products_count=Count('products'))
    serializer_class = collectionserializer
    #...............insted.....................
    # def get(self,request,pk):
    #     collection = get_object_or_404(
    #     Collection.objects.annotate(products_count=Count('products')), pk=pk)
    #     serializer = collectionserializer(collection)
    #     return Response(serializer.data)
    # def put(self,request,pk): 
    #     collection = get_object_or_404 (Collection,pk=pk)
    #     serializer = collectionserializer(collection, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    def delete(self,request,pk):
        collection= get_object_or_404 (Collection,pk=pk)
        if collection.products.count() >0:
            return Response({'error':'collection cannot be deleted '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer
    #...............insted.....................
    # def get(self,request,id):
    #     product= get_object_or_404 (Product,pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    # def put(self,request,id): 
    #     product= get_object_or_404 (Product,pk=id)
    #     serializer= ProductSerializer(product,data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    
    def delete(self,request,pk):
        product= get_object_or_404 (Product,pk=pk)
        if product.orderitems.count() >0:
            return Response({'error':'product cannot be deleted '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

