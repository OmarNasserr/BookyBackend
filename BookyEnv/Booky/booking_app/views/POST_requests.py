from asyncio.windows_events import NULL
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from ..serializers import BookingSerializer
from ..validations import BookingAppValidations
from ..models import Booking
from django.conf import settings
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)

class BookingCreate(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        playgronud_id=aes.decrypt(str(self.kwargs['playground_id']))
        reservationist_id=aes.decrypt(str(request.data['reservationist']))
        request.data._mutable = True
        request.data['playground_id'] = playgronud_id
        request.data['reservationist'] = reservationist_id
        serializer = self.get_serializer(data=request.data)
        valid,err=serializer.is_valid(raise_exception=False)
        response = BookingAppValidations.validate_booking_created(self,request.data,valid,err)
        if response.status_code == 201:
            serializer.save()
            response.data['booking']={
                'booking_id':serializer.data['id'],
                'playground_id':serializer.data['playground_id'],
                'reservationist_id':serializer.data['reservationist'],
                'playground_name':serializer.data['playground_name'],
                'date':serializer.data['date'],
                'start_time':serializer.data['start_time'],
                'end_time':serializer.data['end_time'],
                'booking_hours':serializer.data['booking_hours'],
                'price_paid':serializer.data['total_price_to_be_paid'],
            }
        return response

    
    