from store.models import Collection, Product, Review,Cart
from rest_framework import serializers
from decimal import Decimal

class collectionserializer(serializers.ModelSerializer):
    class Meta:
        model =Collection
        fields =['id','title','products_count']
    
    products_count = serializers.IntegerField(read_only=True)

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
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']
        
    #mortabet kardan review ba id product(id product dar review neveshte mishavad)
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Cart
        fields = ['id','items']
        