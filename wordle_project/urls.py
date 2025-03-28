from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .swagger import schema_view


urlpatterns = [
    path('', lambda request: redirect('/client/')),  # Redirect root to client menu  
    path('admin/', admin.site.urls),  
    path('accounts/', include('allauth.urls')),  
    path('api/game/', include('game.urls')),  

    # Swagger API Docs
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] 

