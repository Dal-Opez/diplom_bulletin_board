from rest_framework.pagination import PageNumberPagination


class AdvertisementPaginator(PageNumberPagination):
    page_size = 2