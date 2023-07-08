from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import re
from helper_files.status_code import Status_code


class UserAppValidation():
    def validate_user_create(data,valid,err):
        
        email_regex="(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|'(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*')@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        
        if valid:
            if data['password_confirm'] != data['password']:
                return Response(data={'message': "password_confirm does not match password.",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)

            if User.objects.filter(email=data['email']).exists():
                return Response(data={'message': "this email already exists.",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            
            if User.objects.filter(username=data['username']).exists():
                return Response(data={'message': "this user already exists.",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            
            if not re.match(email_regex,data['email']):
                return Response(data={'message': "invalid email address.",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            
            if len(data['first_name'])<2:
                return Response(data={'message': "first_name must be at least 2 characters",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            
            if len(data['last_name'])<2:
                return Response(data={'message': "last_name must be at least 2 characters",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
           
            else:
               return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={'message':str(err),"status":Status_code.bad_request},
                                    status=Status_code.bad_request)