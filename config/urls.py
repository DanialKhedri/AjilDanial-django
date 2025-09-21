from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    #core
    path('',include('apps.core.urls')),

    #users
    path('auth/', include('apps.users.urls')),
    
]
