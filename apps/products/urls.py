from django.urls import path
from .views import (
    product_list_view,
    product_detail_view,
    products_by_category_view,
    category_list_view,
)

urlpatterns = [
    path('', product_list_view, name='product_list'),
    path('<slug:slug>/', product_detail_view, name='product_detail'),
    path('category/<slug:slug>/', products_by_category_view, name='products_by_category'),
    path('category/categories/all/', category_list_view, name='category_list'),
]
