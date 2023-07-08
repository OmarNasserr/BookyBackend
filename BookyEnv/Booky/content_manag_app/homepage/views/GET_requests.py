from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from geopy.distance import geodesic

from ..serializers import SliderImageSerializer
from ..models import HomePageSliderImage
from ..pagination import SliderImagePagination


class SliderImageList(generics.ListAPIView):
    serializer_class = SliderImageSerializer
    queryset = HomePageSliderImage.objects.all()

    pagination_class = SliderImagePagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['id']

    def get(self, request, *args, **kwargs):
        SliderImagePagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)