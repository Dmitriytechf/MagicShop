from django.urls import include, path

from .views import about_us, contact

app_name = 'otherapp'

urlpatterns = [
    path('', about_us, name='other'),
    path('contact/', contact, name='contact'),
]
