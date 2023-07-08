from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from ..models import Booking
from ..serializers import BookingSerializer
from ..validations import BookingAppValidations

from helper_files.permissions import AdminOrPlaygroundOwnerOrReservationist
from helper_files.permissions import Permissions
from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes=[AdminOrPlaygroundOwnerOrReservationist]

    def permission_denied(self, request):
        Permissions.permission_denied(self=self ,request=request)

    def check_permissions(self, request):
        try:
            booking_id = aes.decrypt(str(self.kwargs['booking_id']))
            booking=Booking.objects.filter(pk=int(booking_id))
            obj = booking[0]
        except:
            return Response(data={"message": "Booking wasn't found.",
                              "status":Status_code.no_content},status=Status_code.no_content)
        return Permissions.check_object_permissions(self=self,request=request,obj=obj)

    def get_object(self):
        try:
            booking_id = aes.decrypt(str(self.kwargs['booking_id']))
            booking=Booking.objects.filter(pk=int(booking_id))
            obj = booking[0]
        except:
            return ValueError('wrong id format')
        if booking.count() == 0:
            return ValueError('wrong id format')
        return obj

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        if str(type(instance)) != "<class 'booking_app.models.Booking'>":
            return Response(data={"message": "Booking wasn't found.",
                              "status":Status_code.no_content},status=Status_code.no_content)
        else:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)

            valid,err=serializer.is_valid(raise_exception=True)

            request.data._mutable = True
            request.data['playground_id'] = instance.playground_id.id
            response=BookingAppValidations.validate_booking_update(self,self.request.data,valid,err)
            if response.status_code == Status_code.updated:
                serializer.save()
                response.data['booking']=serializer.data

            return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'booking_app.models.Booking'>":
            return Response(data={"message": "Booking wasn't found.",
                              "status":Status_code.no_content},status=Status_code.no_content)
        return super().retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'booking_app.models.Booking'>":
            return Response(data={"message": "Booking wasn't found.",
                              "status":Status_code.no_content},status=Status_code.no_content)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "Booking was deleted successfully.",
                              "status":Status_code.no_content},status=Status_code.no_content)