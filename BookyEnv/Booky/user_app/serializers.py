from dataclasses import fields
from email.policy import default
from django.contrib.auth.models import User
from rest_framework import serializers
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject 
from rest_framework.fields import SkipField
from django.conf import settings
from rest_framework import status

from helper_files.serializer_helper import SerializerHelper
from helper_files.cryptography import AESCipher


aes = AESCipher(settings.SECRET_KEY[:16], 32)


class RegisterationSerializer(serializers.ModelSerializer):
    password_confirm=serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model=User
        fields=['username','email','password','password_confirm','is_staff','first_name','last_name',
                'is_superuser','id']
        extra_kwargs={
            'password':{'write_only':True},
            'email':{'required':True},
            'is_staff':{'default':False},
            'is_superuser':{'default':False},
        }
    
    
    def save(self,validated_data):
        # print("VALID "+str(validated_data))
        # if validated_data['password_confirm'] != validated_data['password']:
        #     raise serializers.ValidationError({'message':'password does not match the password_confirm',
        #                                        'status':status.HTTP_400_BAD_REQUEST})

        # if User.objects.filter(email=validated_data['email']).exists():
        #     raise serializers.ValidationError({'message':'email already exists',
        #                                        'status':status.HTTP_400_BAD_REQUEST})
            
        # if User.objects.filter(username=validated_data['username']).exists():
        #     raise serializers.ValidationError({'message':'username already exists',
        #                                        'status':status.HTTP_400_BAD_REQUEST})        
        
        
        account=User(email=validated_data['email'],username=validated_data['username'],
                     is_staff=validated_data['is_staff'],first_name=validated_data['first_name'],
                     last_name=validated_data['last_name'],
                     is_superuser=validated_data['is_superuser'],)
        account.set_password(validated_data['password'])
        account.save()
        
        return account

    
    def is_valid(self, *, raise_exception=False):
        return SerializerHelper.is_valid(self=self,raise_exception=raise_exception)
    
    def to_representation(self, instance):
        return SerializerHelper.to_representation(
            self=self, instance=instance,
            fields_to_be_decrypted=[],
            fields_to_be_encrypted=['id']
        )
    

class UserSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields
        
        for field in fields:
            try:
                
                attribute = field.get_attribute(instance)
            except SkipField:
                continue
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ## put the attributes that are encrypted in the db and 
                ## you want them to be decrypted
                if field.field_name in ['fields_to_be_encrypted']:
                    ret[field.field_name] = aes.decrypt(field.to_representation(attribute))
                ## pu the attributes that are not encrypted in the db and 
                ## you want them to be showed encrypted (Foriegn Keys, ids, etc)
                elif field.field_name in ['id']:
                    ret[field.field_name] = aes.encrypt(str(field.to_representation(attribute)))
                else:
                    ret[field.field_name] = field.to_representation(attribute)

        return ret 
    
    class Meta:
        model=User
        fields=['username','email','is_staff','first_name','last_name',
                'is_superuser','id']