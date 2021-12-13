from django.urls import path
from django.urls.conf import include
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views
from pprint import pprint

router = DefaultRouter()
router.register('products',views.productViewSet)
router.register('collections',views.collectionViewSet)
# pprint(router.urls)


# URLConf
urlpatterns = [
    path('', include(router.urls)),
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>/', views.ProductDetail.as_view()),
    # path('collections/', views.collectionlist.as_view()),
    # path('collections/<int:pk>/', views.collectionDetail.as_view(), name='collection-detail'),
]
