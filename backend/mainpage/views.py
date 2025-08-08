from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    '''Фукнция отображения главной страници'''
    template_name = 'mainpage/index.html'
