from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import CharFilter, FilterSet
from .models import Advertisement, Review
from .pagination import AdvertisementPaginator
from .serializers import AdvertisementSerializer, ReviewSerializer
from .permissions import IsOwnerOrAdmin


class AdvertisementFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains", label="Название")

    class Meta:
        model = Advertisement
        fields = ["title"]


class AdvertisementListView(generics.ListCreateAPIView):
    queryset = Advertisement.objects.all().order_by("-created_at")
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    pagination_class = AdvertisementPaginator

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdvertisementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]


class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def get_queryset(self):
        return Review.objects.filter(
            advertisement_id=self.kwargs["advertisement_id"]
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, advertisement_id=self.kwargs["advertisement_id"]
        )


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrAdmin,
    ]
