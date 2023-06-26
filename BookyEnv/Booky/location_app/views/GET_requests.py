from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters


from ..models import City
from ..serializers import CitiesSerializer
from ..models import Governorate
from ..serializers import GovSerializer
from ..pagination import LocationPagination

class CitiesList(generics.ListAPIView):
    serializer_class=CitiesSerializer
    queryset=City.objects.all()
    pagination_class=LocationPagination
    
    filter_backends=[filters.SearchFilter]
    search_fields=['city_name']



class GovList(generics.ListAPIView):
    serializer_class=GovSerializer
    queryset=Governorate.objects.all()
    pagination_class=LocationPagination
    
    filter_backends=[filters.SearchFilter]
    search_fields=['gov_name']
