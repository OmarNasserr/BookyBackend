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
from helper_files.status_code import Status_code

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
                              "status":Status_code.no_content},status=Status_code.no_content) 
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
                              "status":Status_code.no_content},status=Status_code.no_content)
        else:    
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            
            valid,err=serializer.is_valid(raise_exception=True)
            response=PlaygroundAppValidations.validate_playground_update(self.request.data,valid,err)
            if response.status_code == Status_code.updated:
                serializer.save()
                response.data['playground']=serializer.data

            return response

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        response = self.retrieve(request, *args, **kwargs)
        response.data['status']=status.HTTP_200_OK
        response.data['hours_available']=PlaygroundSerializerHelper.get_all_available_paired_hours(
                                            instance,request.data['date'])
        return response

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'playground_app.models.Playground'>":
            return Response(data={"message": "Playground wasn't found.",
                              "status":Status_code.no_content},status=Status_code.no_content)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "Playground was deleted successfully.",
                              "status":Status_code.no_content},status=Status_code.no_content)