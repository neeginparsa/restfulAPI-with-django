from store.models import Collection, Product
from rest_framework import serializers
from decimal import Decimal

class collectionserializer(serializers.ModelSerializer):
    class Meta:
        model =Collection
        fields =['id','title','products_count']
    
    products_count = serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','slug','inventory','price','price_with_tax','collection']
    # id = serializers.IntegerField()
    # title= serializers.CharField(max_length = 250)
    price=serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax= serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.StringRelatedField()   #avardan str function collection az model be api
   
    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)