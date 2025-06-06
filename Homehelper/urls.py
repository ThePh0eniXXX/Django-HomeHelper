from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from users.views import GroupCreateView, GroupMembersView, GroupJoinView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from rest_framework.authentication import BasicAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="HomeHelper API",
        default_version='v1',
        description="Документация API для приложения HomeHelper",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="you@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # ВАЖНО!
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # ← ЭТО ДОБАВЬ
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    #Tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/group/create/', GroupCreateView.as_view(), name='group-create'),
    path('api/group/members/', GroupMembersView.as_view(), name='group-members'),
    path('api/group/join/', GroupJoinView.as_view(), name='group-join'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


