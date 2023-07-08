from rest_framework import generics
from ..models import HomePageSliderImage
from ..serializers import SliderImageSerializer
from helper_files.permissions import AdminOnly
from helper_files.status_code import Status_code
from ..validations import HomaPageValidations


class SliderImageCreate(generics.CreateAPIView):
    queryset = HomePageSliderImage.objects.all()
    serializer_class = SliderImageSerializer
    # permission_classes=[AdminOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        valid,err=serializer.is_valid(raise_exception=False)
        response = HomaPageValidations.validate_slider_image_create(self.request.data,valid,err)
        if response.status_code == Status_code.created:
            serializer.save()

        return response