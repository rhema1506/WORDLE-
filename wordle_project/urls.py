from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect

from .swagger import schema_view

def redirect_to_admin(request):
    return redirect('/admin/')

urlpatterns = [
    path('', redirect_to_admin, name='home'),
    path('admin/', admin.site.urls),

    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),

    # Game API
    path('api/game/', include('game.urls')),

    # API documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
