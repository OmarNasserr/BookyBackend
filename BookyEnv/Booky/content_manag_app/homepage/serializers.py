from rest_framework import serializers
import datetime

from .models import HomePageSliderImage
from helper_files.serializer_helper import SerializerHelper


class SliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageSliderImage
        fields = ["id", "image",]

    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self,raise_exception=raise_exception)
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )