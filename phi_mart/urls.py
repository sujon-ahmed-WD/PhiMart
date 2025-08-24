from django.contrib import admin
from django.urls import path,include
from .views import api_root_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',api_root_view),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('api/v1/', include('api.urls'),name='api-root'),
    
]