from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from ..serializers import SliderImageSerializer
from ..models import HomePageSliderImage
from helper_files.permissions import AdminOnly, Permissions

from django.conf import settings
from helper_files.cryptography import AESCipher
from helper_files.status_code import Status_code
from helper_files.serializer_helper import SerializerHelper
from ..validations import HomaPageValidations

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class SliderImageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SliderImageSerializer
    # permission_classes = [AdminOnly]

    def permission_denied(self, request):
        Permissions.permission_denied(self=self, request=request)

    def check_permissions(self, request):
        try:
            slider_image_id = aes.decrypt(str(self.kwargs['slider_image_id']))
            print("ID ",slider_image_id)
            slider_image = HomePageSliderImage.objects.filter(pk=int(slider_image_id))
            obj = slider_image[0]
        except:
            return Response(data={"message": "Slider image wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        return Permissions.check_object_permissions(self=self, request=request, obj=obj)

    def get_object(self):
        try:
            slider_image_id = aes.decrypt(str(self.kwargs['slider_image_id']))
            slider_image = HomePageSliderImage.objects.filter(pk=int(slider_image_id))
            obj = slider_image[0]
            print(type(obj))
        except:
            return ValueError('wrong id format')
        if slider_image.count() == 0:
            return ValueError('wrong id format')
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'content_manag_app.homepage.models.HomePageSliderImage'>":
            return Response(data={"message": "Slider image wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        else:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            valid,err=serializer.is_valid(raise_exception=False)
            response = HomaPageValidations.validate_slider_image_create(self.request.data, valid, err,create=False)
            if response.status_code == Status_code.created:
                self.perform_update(serializer)
                # By clearing the prefetch cache, the code guarantees that only the most
                # up-to-date data is used during the update operation, without any interference
                # from cached or prefetched objects.
                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                response.data['image']=serializer.data
                return response
            else:
                return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        str(type(instance))
        if str(type(instance)) != "<class 'content_manag_app.homepage.models.HomePageSliderImage'>":
            return Response(data={"message": "Slider image wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(type(instance)) != "<class 'content_manag_app.homepage.models.HomePageSliderImage'>":
            return Response(data={"message": "Slider image wasn't found.",
                                  "status": Status_code.no_content}, status=Status_code.no_content)
        super().delete(request, *args, **kwargs)
        return Response(data={"message": "Slider image was deleted successfully.",
                              "status": Status_code.no_content}, status=Status_code.no_content)