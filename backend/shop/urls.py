from django.urls import include, path

from .views import category_list, product_detail, products_view

app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('product/<slug:slug>/', product_detail, name='product-detail'),
    path('search/<slug:slug>/', category_list, name='category-list')
]
