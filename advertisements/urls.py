from django.urls import path
from .views import (
    AdvertisementListView,
    AdvertisementDetailView,
    ReviewListView,
    ReviewDetailView
)

urlpatterns = [
    path('', AdvertisementListView.as_view(), name='advertisement-list'),
    path('<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement-detail'),
    path('<int:advertisement_id>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('<int:advertisement_id>/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]