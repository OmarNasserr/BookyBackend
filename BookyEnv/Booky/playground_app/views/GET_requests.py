from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from geopy.distance import geodesic

from ..serializers import PlaygroundSerializer,PlaygroundListAllSerializer
from ..models import Playground
from ..pagination import PlaygroundPagination


class PlaygroundList(generics.ListAPIView):
    serializer_class = PlaygroundListAllSerializer
    queryset = Playground.objects.all()
    
    pagination_class=PlaygroundPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields=['p_name', 'city__city_name','city__governorate',
                     'open_time', 'close_time', 'price_per_hour','id']
    search_fields = ['p_name', 'city__city_name',
                     'open_time', 'close_time', 'price_per_hour','city__governorate__gov_name',]
    
    def get(self, request, *args, **kwargs):
        PlaygroundPagination.set_default_page_number_and_page_size(request)
        return super().get(request, *args, **kwargs)
    


#this class view is used to return nearest playgrounds to the user, and the user can control
#max KMs playgrounds can be
#for ex if request.data['distance'] is 5 then the queryset will contain only playgrounds that
#are within range 0-5 KMs away
class NearestPLaygrounds(generics.ListAPIView):
    serializer_class = PlaygroundListAllSerializer
    queryset = Playground.objects.all()
    
    pagination_class=PlaygroundPagination
    
    
    def get(self, request, *args, **kwargs):
        PlaygroundPagination.set_default_page_number_and_page_size(request)
        queryset = self.filter_queryset(self.get_queryset())
        lat,long=str(request.data['location']).split(',')
        user_location=(str(float(lat))+","+str(float(long)))
        
        nearest_playgrounds=set()
        for query in queryset:
            lat,long=str(query.location).split(',')
            playground_location=(str(float(lat))+","+str(float(long)))
            kilometers = geodesic(user_location,playground_location).kilometers
            print("KIL ",kilometers)
            if kilometers<=int(request.data['distance']):
                nearest_playgrounds.add(query.pk)

        
        returned_query=Playground.objects.filter(pk__in=nearest_playgrounds)
        

        page = self.paginate_queryset(returned_query)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(returned_query, many=True)
        return Response(serializer.data)
    
