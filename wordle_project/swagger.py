from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Wordle Game API",
        default_version="v1",
        description="API for playing Wordle, designed for client-server communication.",
        terms_of_service="https://yourwebsite.com/terms/",
        contact=openapi.Contact(email="support@wordlegame.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Add Java client SDK generation  
schema_view.without_ui(cache_timeout=0), name="schema-json"  
schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"  
schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"  
