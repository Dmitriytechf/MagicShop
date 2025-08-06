from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Category, ProductProxy


def products_view(request):
    '''
    Функция показывает главную страницу с товарами. Реализует действия поиска
    или возвращает все товары(базовый случай), создает пагинацию, если товаров
    больше 9.
    '''
    query = request.GET.get('q')
    if query:
        products_list = ProductProxy.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    else:
        products_list = ProductProxy.objects.all()

    # Pagination
    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(
        request, 
        'shop/products.html', 
        {'products': products,
         'search_query': query})


def product_detail(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    subcategories = category.children.all()
    
    context = {
        'category': category,
        'products': products,
        'subcategories':subcategories,
        'parent_category': category.parent
    }
    return render(request, 'shop/category_list.html', context)
