from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from ..serializers import CitiesSerializer,GovSerializer
from ..models import City,Governorate
from helper_files.permissions import AdminOnly,Permissions

from django.conf import settings
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CitiesSerializer
    permission_classes=[AdminOnly]
    
    def permission_denied(self, request):
        Permissions.permission_denied(self=self ,request=request)
    
    def check_permissions(self, request):
        try:
            city_id = aes.decrypt(str(self.kwargs['city_id']))
            city=City.objects.filter(pk=int(city_id))
            obj = city[0]
        except:
            return Response(data={"message": "City wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT) 
        return Permissions.check_object_permissions(self=self,request=request,obj=obj)
    
    def get_object(self):
        try:
            city_id = aes.decrypt(str(self.kwargs['city_id']))
            city=City.objects.filter(pk=int(city_id))
            obj = city[0]
            print(type(obj))
        except:
            return ValueError('wrong id format')
        if city.count() == 0:
            return ValueError('wrong id format')
        self.check_object_permissions(self.request, obj)
        return obj
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'location_app.models.City'>":
            return Response(data={"message": "City wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'location_app.models.City'>":
            return Response(data={"message": "City wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'location_app.models.City'>":
            return Response(data={"message": "City wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "City was deleted successfully.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)
        
class GovDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GovSerializer
    permission_classes=[AdminOnly]
    
    def permission_denied(self, request):
        Permissions.permission_denied(self=self ,request=request)
    
    def check_permissions(self, request):
        try:
            gov_id = aes.decrypt(str(self.kwargs['gov_id']))
            gov=Governorate.objects.filter(pk=int(gov_id))
            obj = gov[0]
        except:
            return Response(data={"message": "Governorate wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT) 
        return Permissions.check_object_permissions(self=self,request=request,obj=obj)
    
    def get_object(self):
        try:
            gov_id = aes.decrypt(str(self.kwargs['gov_id']))
            gov=Governorate.objects.filter(pk=int(gov_id))
            obj = gov[0]
            print(type(obj))
        except:
            return ValueError('wrong id format')
        if gov.count() == 0:
            return ValueError('wrong id format')
        self.check_object_permissions(self.request, obj)
        return obj
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'location_app.models.Governorate'>":
            return Response(data={"message": "Governorate wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'location_app.models.Governorate'>":
            return Response(data={"message": "Governorate wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'location_app.models.Governorate'>":
            return Response(data={"message": "Governorate wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "Governorate was deleted successfully.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)