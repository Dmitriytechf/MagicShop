from django.shortcuts import render


def about_us(request):
    '''Страница О нас'''
    return render(request, 'otherapp/about_us.html')


def contact(request):
    '''Страница Контакты'''
    return render(request, 'otherapp/contact.html')
