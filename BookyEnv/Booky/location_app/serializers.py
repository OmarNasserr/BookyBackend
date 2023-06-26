from rest_framework import serializers
from .models import City
from .models import Governorate
from playground_app.serializers import PlaygroundSerializer  
from helper_files.serializer_helper import SerializerHelper




class CitiesSerializer(serializers.ModelSerializer):
    playgrounds=serializers.StringRelatedField(many=True,read_only=True)
    # playgrounds=PlaygroundSerializer(many=True,read_only=True)
    playground_owner=serializers.StringRelatedField(many=True,read_only=True)
    
    class Meta:
        model=City
        fields='__all__'
        
    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self, raise_exception=raise_exception)
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['number_of_playgrounds']=len(ret['playgrounds'])
        print(ret['number_of_playgrounds'])
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id'],
            fields_to_be_added={'number_of_playgrounds':len(ret['playgrounds'])}
        )
        
    
        
        
    
            

class GovSerializer(serializers.ModelSerializer):
    
    city=CitiesSerializer(many=True,read_only=True,) #this shows all cities with details
    # city=serializers.StringRelatedField(many=True,read_only=True) #this will show only city name

    class Meta:
        model=Governorate
        fields='__all__'
        
    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self,raise_exception=raise_exception)
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )
    
            
