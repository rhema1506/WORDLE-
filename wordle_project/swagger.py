from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Wordle Game API",
        default_version="v1",
        description="API documentation for Wordle Game",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)




openapi.Info(
    title="Wordle Game API",
    default_version="v1",
    description="""
    ## **Client Menu**  
    -  **Start Game**: `/client/start/` → Fetch the daily word.  
    -  **Make a Guess**: `/client/end/` → Submit a word guess.  
    -  **API Docs (Swagger)**: `/swagger/`  
    - **API Docs (ReDoc)**: `/redoc/`  
    """,
)
