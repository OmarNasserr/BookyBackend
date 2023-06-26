from rest_framework.exceptions import  ValidationError
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject
from rest_framework.fields import SkipField
from django.conf import settings

from .cryptography import AESCipher


aes = AESCipher(settings.SECRET_KEY[:16], 32)

class SerializerHelper():
    
    
    #is_valid is overrided to return bool and a error value if exist, this is done to keep a 
    #consistent response shape {'message':'xxx',...}, therefore the error message is extracted
    #and returned to the response to be represented in a proper format.
    def is_valid(self, *, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)
        
        if len(self.errors.keys())!=0:
            print(self._errors)
            err=list(self.errors.keys())[0]
            if self.errors[str(err)][0]=="This field is required.":
                errReturned="The field '"+str(err)+"' is required"
            else:
                errReturned=self.errors[str(err)][0]
        else:
            errReturned="no errors were returned"

        return not bool(self._errors),errReturned
    
    
    # to_representation function is used to represent data in response, and as we might have 
    # returned encrypted data or data that we would like to be represented as encrypted data 
    # like object_id
    # therefore the fields_to_be_decrypted is a list of fields that are stored in db encrypted
    # and we would like to decrypt and represent them
    # fields_to_be_encrypted is list of fields that aren't encrypted in the database but they
    # are sensitive, therefore we need to encrypt them in the response
    def to_representation(
        self, instance,
        fields_to_be_decrypted,
        fields_to_be_encrypted,
        fields_to_be_added={}
    ):
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
                if field.field_name in fields_to_be_decrypted:
                    ret[field.field_name] = aes.decrypt(field.to_representation(attribute))
                ## put the attributes that are not encrypted in the db and 
                ## you want them to be showed encrypted (Foriegn Keys, ids, etc)
                elif field.field_name in fields_to_be_encrypted:
                    ret[field.field_name] = aes.encrypt(str(field.to_representation(attribute)))
                else:
                    ret[field.field_name] = field.to_representation(attribute)
        if fields_to_be_added is not {}:
            for key in fields_to_be_added.keys():
                ret[str(key)] = fields_to_be_added[str(key)]

        return ret