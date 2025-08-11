from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('mainpage.urls')), # главная страница примерно как в играх
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('shop.urls', namespace='shop')),
    path('account/', include('account.urls', namespace='account')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('other/', include('otherapp.urls', namespace='otherapp')),
    path('api/v1/', include('api.urls', namespace='api'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
