from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, ProductProxy


def products_view(request):
    '''
    Функция показывает главную страницу с товарами. Реализует действия поиска
    или возвращает все товары(базовый случай), создает пагинацию, если товаров
    больше 9.
    '''
    query = request.GET.get('q')
    if query:
        # Поиск по назавнию и описанию
        products_list = ProductProxy.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    else:
        products_list = ProductProxy.objects.all()

    # Фильтры
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products_list = products_list.filter(price__gte=min_price)
    if max_price:
        products_list = products_list.filter(price__lte=max_price)

    if request.GET.get('available'):
        products_list = products_list.filter(available=True)

    # Сортировка
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort == 'price_desc':
        products_list = products_list.order_by('-price')
    elif sort == 'newest':
        products_list = products_list.order_by('-created_at')

    # Pagination
    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'shop/_partials/products_list.html', {
            'products': products,
            'search_query': query
        })

    return render(
        request, 
        'shop/products.html',
        {'products': products,
         'search_query': query})


def product_detail(request, slug):
    '''
    Функция показывает страницу отдельного товара
    '''
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
