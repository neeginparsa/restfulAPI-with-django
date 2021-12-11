from typing import Counter
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Count
from rest_framework import status
from .models import Collection, Product
from .serializers import ProductSerializer,collectionserializer
from store import serializers

class ProductList(APIView):
    def get(self,request):
        querySet= Product.objects.select_related('collection').all() #select_related--> baraye farakhani fieldi az classe digar
        serializer= ProductSerializer(querySet,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer= ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class collectionlist(APIView):
    def get(self,request):
        querySet= Collection.objects.annotate(products_count=Count('products')).all() 
        serializer= collectionserializer(querySet,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer= collectionserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class collectionDetail(APIView):
    def get(self,request,id):
        collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count('products')), pk=id)
        serializer = collectionserializer(collection)
        return Response(serializer.data)
    def put(self,request,id): 
        collection = get_object_or_404 (Collection,pk=id)
        serializer = collectionserializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,id):
        collection= get_object_or_404 (Collection,pk=id)
        if collection.orderitem_set.count() >0:
            return Response({'error':'collection cannot be deleted '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductDetail(APIView):
    def get(self,request,id):
        product= get_object_or_404 (Product,pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    def put(self,request,id): 
        product= get_object_or_404 (Product,pk=id)
        serializer= ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,id):
        product= get_object_or_404 (Product,pk=id)
        if Product.orderitems_set.count() >0:
            return Response({'error':'product cannot be deleted '},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

