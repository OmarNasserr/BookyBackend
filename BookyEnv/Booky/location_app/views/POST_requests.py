from asyncio.windows_events import NULL
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from ..serializers import CitiesSerializer
from ..models import City,Governorate
from ..serializers import GovSerializer
from ..validations import LocationAppValidations
from helper_files.permissions import AdminOnly



class GovCreate(generics.CreateAPIView):
    queryset=Governorate.objects.all()
    serializer_class=GovSerializer
    permission_classes= [AdminOnly]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        valid,err=serializer.is_valid(raise_exception=False)
        
        response = LocationAppValidations.validate_gov_create(self.request.data,valid,err)
        if response.status_code==201:
            serializer.save()
            
        return response 

class CityCreate(generics.CreateAPIView):
    queryset=City.objects.all()
    serializer_class=CitiesSerializer
    # permission_classes=[AdminOnly]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        valid,err=serializer.is_valid(raise_exception=False)
        
        response = LocationAppValidations.validate_city_create(self.request.data,valid,err)
        if response.status_code==201:   
            serializer.save()
            
        return response 