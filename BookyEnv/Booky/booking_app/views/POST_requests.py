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
from helper_files.status_code import Status_code

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
        if response.status_code == Status_code.created:
            serializer.save()
            response.data['booking'] = {
                key: serializer.data[key] for key in serializer.data.keys()
            }
        return response

    
    