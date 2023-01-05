from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from engine.views import UserRecipeView, AllRecipes
from users.views import Register, ObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),

    # authentication urls
    path('api/v1/register/', Register.as_view(), name='register'),
    path('api/v1/login/', ObtainAuthToken.as_view(), name='login'),

    # Recipe APIs
    path('api/v1/recipes/', UserRecipeView.as_view(), name="UserRecipeView"),
    path('api/v1/recipes/all/', AllRecipes.as_view(), name="AllRecipes")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
