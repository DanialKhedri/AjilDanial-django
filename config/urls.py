from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #core
    path('',include('apps.core.urls')),

    #users
    path('auth/', include('apps.users.urls')),


    #products
    path('products/',include('apps.products.urls')),

      #cart
    path('cart/',include('apps.cart.urls'))
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)