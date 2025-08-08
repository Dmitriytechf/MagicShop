from django.urls import include, path

from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
