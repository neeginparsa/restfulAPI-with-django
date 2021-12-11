from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetail.as_view()),
    path('collections/', views.collectionlist.as_view()),
    path('collections/<int:id>/', views.collectionDetail.as_view(), name='collection-detail'),
]
