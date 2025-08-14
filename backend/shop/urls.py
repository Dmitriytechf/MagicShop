from django.urls import include, path

from .views import (category_list, delete_review, product_detail, 
                    products_view, edit_review)

app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('product/<slug:slug>/', product_detail, name='product-detail'),
    path('reviews/delete/<int:pk>/', delete_review, name='delete-review'),
    path('review/edit/<int:pk>/', edit_review, name='edit-review'), 
    path('search/<slug:slug>/', category_list, name='category-list')
]
