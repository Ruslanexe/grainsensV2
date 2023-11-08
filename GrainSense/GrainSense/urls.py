from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.OwnerView.as_view(), name='register'),
    path('get_owner/', views.OwnerView.as_view(), name='get_owner'),
    path('post_seed_type/', views.SeedTypesView.as_view(), name='post_seed_type'),
    path('put_seed_type/<int:id>', views.SeedTypesView.as_view(), name='put_seed_type'),
    path('delete_seed_type/<int:id>', views.SeedTypesView.as_view(), name='delete_seed_type'),
    path('get_seed_type/', views.SeedTypesView.as_view(), name='get_seed_type'),
    path('post_storage/', views.StorageView.as_view(), name='post_storage'),
    path('get_storage/', views.StorageView.as_view(), name='get_storage'),
    path('post_gateway/', views.GatewayView.as_view(), name='post_gateway'),
    path('get_gateway/', views.GatewayView.as_view(), name='get_gateway'),
    path('post_stick/', views.StickView.as_view(), name='post_stick'),
    path('get_sticks/', views.StickView.as_view(), name='get_sticks'),
    path('get_entries/', views.EntryView.as_view(), name='get_entries'),
    path('post_entry/', views.EntryView.as_view(), name='post_entry'),
    path('login/', views.LoginView.as_view(), name='login')
]
