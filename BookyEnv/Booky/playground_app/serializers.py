from rest_framework import serializers
import datetime

from .models import Playground, PlaygroundImage
from .helper import PlaygroundSerializerHelper
from helper_files.serializer_helper import SerializerHelper
from helper_files.cryptography import AESCipher
from django.conf import settings

aes = AESCipher(settings.SECRET_KEY[:16], 32)


class PlaygroundImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaygroundImage
        fields = ["id", "image", "thumbnail", ]

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )


class PlaygroundSerializer(serializers.ModelSerializer):
    governorate = serializers.SerializerMethodField('get_gov_from_city')
    p_owner_id = serializers.SerializerMethodField('get_playground_owner_id')
    images = PlaygroundImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, use_url=False),
        write_only=True,
    )

    class Meta:
        model = Playground
        # fields = '__all__'
        exclude = ('created_at', 'updated_at',)

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('p_name', 'city'),
                message="This playground name is already used in this city."
            )
        ]

    def get_gov_from_city(self, playground):
        gov = playground.city.governorate.gov_name
        return gov

    def get_playground_owner_id(self, playground):
        owner_id=playground.playground_owner.id
        return aes.encrypt(str(owner_id))

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        playground = Playground.objects.create(**validated_data)

        create_thumbnail = True
        for image in uploaded_images:
            PlaygroundImage.objects.create(playground=playground, image=image, thumbnail=create_thumbnail)

        return playground

    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self, raise_exception=raise_exception)

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )


class PlaygroundListAllSerializer(serializers.ModelSerializer):
    governorate = serializers.SerializerMethodField('get_gov_from_city')
    p_owner_id = serializers.SerializerMethodField('get_playground_owner_id')
    images = PlaygroundImageSerializer(many=True, read_only=True, )

    class Meta:
        model = Playground
        # fields = '__all__'
        exclude = ('created_at', 'updated_at',)

    def get_gov_from_city(self, playground):
        gov = playground.city.governorate.gov_name
        return gov

    def get_playground_owner_id(self, playground):
        owner_id=playground.playground_owner.id
        print("OWNER ", owner_id)
        return aes.encrypt(str(owner_id))

    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )
