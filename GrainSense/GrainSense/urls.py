from . import views

from django.urls import re_path, path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="GrainSense API",
        default_version='v27',
        description="Welcome v glaz or v jopu raz",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('register/', views.register, name='register'),
    path('get_owner/<int:http_user>/<str:http_token>/<str:http_expires>/', views.get_owner, name='get_owner'),
    path('post_seed_type/', views.post_seed_type, name='post_seed_type'),
    path('get_seed_type/', views.get_seed_type, name='get_seed_type'),
    path('get_seed_type/<int:id>', views.get_seed_type, name='get_seed_type'),
    path('post_storage/<int:http_user>/<str:http_token>/<str:http_expires>/', views.post_storage, name='post_storage'),
    path('get_storage/<int:http_user>/<str:http_token>/<str:http_expires>/', views.get_storage, name='get_storage'),
    path('post_gateway/<int:http_user>/<str:http_token>/<str:http_expires>/', views.post_gateway, name='post_gateway'),
    path('get_gateways/<int:http_user>/<str:http_token>/<str:http_expires>/', views.get_gateway, name='get_gateways'),
    path('post_stick/<int:http_user>/<str:http_token>/<str:http_expires>/', views.post_stick, name='post_stick'),
    path('get_sticks/<int:gateway_id>/<int:http_user>/<str:http_token>/<str:http_expires>/', views.get_sticks, name='get_sticks'),
    path('get_entries/<int:storage_id>/<int:http_user>/<str:http_token>/<str:http_expires>/', views.get_entry, name='get_entries'),
    path('post_entry/<int:http_user>/<str:http_token>/<str:http_expires>/', views.post_entry, name='post_entry'),
    path('login/<str:email>/<str:password>/', views.login, name='login')
]
