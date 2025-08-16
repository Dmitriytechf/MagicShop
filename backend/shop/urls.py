from django.urls import include, path

from .views import (category_list, delete_review, edit_review, product_detail,
                    products_view, favorite_list, toggle_favorite)

app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('product/<slug:slug>/', product_detail, name='product-detail'),
    path('toggle-favorite/<int:product_id>/', toggle_favorite, name='toggle-favorite'),
    path('favorites/', favorite_list, name='favorites'),
    path('reviews/delete/<int:pk>/', delete_review, name='delete-review'),
    path('review/edit/<int:pk>/', edit_review, name='edit-review'), 
    path('search/<slug:slug>/', category_list, name='category-list')
]
