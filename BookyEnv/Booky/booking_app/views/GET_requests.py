from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..pagination import BookingPagination


from ..serializers import BookingSerializer
from ..models import Booking

class BookingsList(generics.ListAPIView):
    serializer_class=BookingSerializer
    queryset=Booking.objects.all()
    pagination_class=BookingPagination
    
    def get(self, request, *args, **kwargs):
        BookingPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields=['playground_id__p_name','reservationist__username','date',
                     'booking_hours', 'total_price_to_be_paid']
    search_fields = ['playground_id__p_name', 'reservationist__username','date',
                     'booking_hours', 'total_price_to_be_paid']

