from django.urls import path
from . import views

urlpatterns = [
    path('post_owner/', views.OwnerView.as_view(), name='post_owner'),
    path('get_owner/', views.OwnerView.as_view(), name='get_owner'),
    path('get_owner/<int:id>', views.OwnerView.as_view(), name='get_owner'),
    path('post_seed_type/', views.SeedTypesView.as_view(), name='post_seed_type'),
    path('put_seed_type/<int:id>', views.SeedTypesView.as_view(), name='put_seed_type'),
    path('delete_seed_type/<int:id>', views.SeedTypesView.as_view(), name='delete_seed_type'),
    path('get_seed_type/', views.SeedTypesView.as_view(), name='get_seed_type'),
    path('get_seed_type/<int:id>', views.SeedTypesView.as_view(), name='get_seed_type'),
    path('post_storage/', views.StorageView.as_view(), name='post_storage'),
    path('post_gateway/', views.GatewayView.as_view(), name='post_gateway'),
    path('post_stick/', views.StickView.as_view(), name='post_stick'),
    path('get_storage_by_owner/', views.StorageView.as_view(), name='get_storage_by_owner'),
    path('get_entries/<int:storage_id>/<str:start>/<str:finish>', views.EntryView.as_view(), name='get_entries'),
    path('get_entries/<int:storage_id>', views.EntryView.as_view(), name='get_entries'),
    path('get_sticks_by_gateway/<int:gateway_id>', views.StickView.as_view(), name='get_sticks'),
]
