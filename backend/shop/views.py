import random
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .forms import ReviewForm
from .models import Category, ProductProxy, Review, Favorite


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
    и отзывы покупателей к продукту.
    '''
    product = get_object_or_404(ProductProxy, slug=slug)
    # Достаем все отзывы
    all_reviews = product.reviews.all()

    # Проверяем, есть ли товар в избранном у пользователя
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(
            user=request.user, 
            product=product
        ).values_list('product_id', flat=True)

    # Пагинация
    page = request.GET.get('page', 1)
    paginator = Paginator(all_reviews, 5)
    reviews = paginator.get_page(page)

    # Обработка отзывов
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = request.user
            review.save()
            return redirect('shop:product-detail', slug=slug)
    else:
        form = ReviewForm()

    # Получаем случайный товар / исключаем текущий
    all_product = ProductProxy.objects.exclude(id=product.id)
    random_product = random.choice(all_product) if all_product.exists() else None

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'total_reviews': all_reviews.count(),
        'random_product': random_product,
        'user_favorites': user_favorites
        }

    return render(request, 'shop/product_detail.html', context)


@login_required
def edit_review(request, pk):
    '''Функция редактирования отзыва'''
    review = get_object_or_404(Review, pk=pk)
    product_slug = review.product.slug

    # Проверка что пользователь - автор отзыва. Лучше оставить, так безопаснее
    if request.user != review.author:
        return redirect('shop:product-detail', slug=product_slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('shop:product-detail', slug=product_slug)
    else:
        form = ReviewForm(instance=review)

    context = {
        'product': review.product,
        'reviews': review.product.reviews.all(),
        'form': form,
        'editing_review': review.id
    }

    return render(request, 'shop/product_detail.html', context)


@require_POST
@login_required
def delete_review(request, pk):
    '''Функция удаления отзыва'''
    review = get_object_or_404(Review, pk=pk)
    product_slug = review.product.slug
    # Проверка пользователя на авторство
    if request.user == review.author:
        review.delete()

    return redirect('shop:product-detail', slug=product_slug)


@login_required
def toggle_favorite(request, product_id):
    '''Функция добавления в избранное'''
    if request.method == 'POST':
        product = get_object_or_404(ProductProxy, id=product_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed', 'is_favorite': False})

        return JsonResponse({'status': 'added', 'is_favorite': True})

    return JsonResponse({'status': 'error'}, status=400)


@login_required
def favorite_list(request):
    '''Функция возвращает страницу избранных товаров пользователя'''
    favorites = Favorite.objects.filter(user=request.user).select_related('product')

    paginator = Paginator(favorites, 5)
    page_number = request.GET.get('page')
    favorite_list = paginator.get_page(page_number)

    context = {
        'favorite_list': favorite_list,
        'title': 'Мои избранные товары'
    }

    return render(request, 'shop/favorites.html', context)


def category_list(request, slug):
    '''Фукнция показыает странички с категориями товаров'''
    category = get_object_or_404(Category, slug=slug)
    # Достаем продукты определенной категории
    products = ProductProxy.objects.select_related('category').filter(category=category)
    subcategories = category.children.all()

    # Все категории и подкатегории в контекст
    context = {
        'category': category,
        'products': products,
        'subcategories':subcategories,
        'parent_category': category.parent
    }
    return render(request, 'shop/category_list.html', context)
