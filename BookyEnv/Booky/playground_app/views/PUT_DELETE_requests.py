from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from ..models import Playground
from ..serializers import PlaygroundSerializer
from ..validations import PlaygroundAppValidations
from ..helper import PlaygroundSerializerHelper
from helper_files.permissions import AdminOrPlaygroundOwner,Permissions

from django.conf import settings
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class PlaygroundDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaygroundSerializer
    permission_classes=[AdminOrPlaygroundOwner]
    
    def permission_denied(self, request):
        Permissions.permission_denied(self=self ,request=request)
    
    def check_permissions(self, request):
        try:
            playground_id = aes.decrypt(str(self.kwargs['playground_id']))
            playground=Playground.objects.filter(pk=int(playground_id))
            obj = playground[0]
        except:
            return Response(data={"message": "Playground wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT) 
        return Permissions.check_object_permissions(self=self,request=request,obj=obj)
    
    def get_object(self):
        try:
            playground_id = aes.decrypt(str(self.kwargs['playground_id']))
            playgronud=Playground.objects.filter(pk=int(playground_id))
            obj = playgronud[0]
            print(type(obj))
        except:
            return ValueError('wrong id format')
        if playgronud.count() == 0:
            return ValueError('wrong id format')
        self.check_object_permissions(self.request, obj)
        return obj
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'playground_app.models.Playground'>":
            return Response(data={"message": "Playground wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)
        else:    
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            
            valid,err=serializer.is_valid(raise_exception=True)
            response=PlaygroundAppValidations.validate_playground_update(self.request.data,valid,err)
            if response.status_code == 202:
                serializer.save()
                response.data['playground']=serializer.data
                print(response.data["playground"])

            return response
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'playground_app.models.Playground'>":
            return Response(data={"message": "Playground wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(instance)
        print(serializer.data)
        return Response(data={
                    "status":status.HTTP_200_OK,
                    "id": serializer.data['id'],
                    "governorate": serializer.data['governorate'],
                    "p_name": serializer.data['p_name'],
                    "open_time": serializer.data['open_time'],
                    "close_time": serializer.data['close_time'],
                    "total_available_time": serializer.data['total_available_time'],
                    "description": serializer.data['description'],
                    "price_per_hour": serializer.data['price_per_hour'],
                    "city": serializer.data['city'],
                    "playground_owner": serializer.data['playground_owner'],
                    "images": serializer.data['images'],
                    "hours_avaialble": PlaygroundSerializerHelper.get_all_available_paired_hours(
                                            instance,request.data['date']),},
                        status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'playground_app.models.Playground'>":
            return Response(data={"message": "Playground wasn't found.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "Playground was deleted successfully.",
                              "status":status.HTTP_204_NO_CONTENT},status=status.HTTP_204_NO_CONTENT)