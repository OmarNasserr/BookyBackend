from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings

from ..pagination import BookingPagination
from ..helper import BookingAppHelper

from ..serializers import BookingSerializer
from ..models import Booking
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from helper_files.validations import GeneralValidations

aes = AESCipher(settings.SECRET_KEY[:16], 32)

class BookingsList(generics.ListAPIView):
    serializer_class=BookingSerializer
    queryset=Booking.objects.all()
    pagination_class=BookingPagination

    def get(self, request, *args, **kwargs):
        BookingPagination.set_default_page_number_and_page_size(request)
        try:
            bookings=super().get(request, *args, **kwargs)
        except Exception as err:
            return GeneralValidations.displayErrMessage(err)
        # Convert the data to a queryset of Booking objects
        booking_ids = [aes.decrypt(str(booking['id'])) for booking in bookings.data['results']]
        bookings_queryset = Booking.objects.filter(id__in=booking_ids)
        unexpired=BookingAppHelper.check_expired_bookings(bookings_queryset)
        unexpired_serialized = self.serializer_class(unexpired, many=True).data
        bookings.data['results']=unexpired_serialized
        return bookings
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields=['playground_id__p_name','reservationist__username','date',
                     'booking_hours', 'total_price_to_be_paid','payment_status']
    search_fields = ['playground_id__p_name', 'reservationist__username','date',
                     'booking_hours', 'total_price_to_be_paid','payment_status']

