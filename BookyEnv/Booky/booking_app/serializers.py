from rest_framework import serializers


from .models import Booking
from helper_files.serializer_helper import SerializerHelper


class BookingSerializer(serializers.ModelSerializer):
    playground_name = serializers.SerializerMethodField('get_booked_playground_name')
    
    def get_booked_playground_name(self,booking):
        p_name=booking.playground_id.p_name
        return p_name
    
    class Meta:
        model = Booking
        fields = '__all__'

    
    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self,raise_exception=raise_exception)
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id',"playground_id","reservationist"]
        )