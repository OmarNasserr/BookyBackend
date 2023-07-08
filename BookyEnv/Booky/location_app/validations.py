from rest_framework.response import Response
from rest_framework import status
from helper_files.status_code import Status_code

class LocationAppValidations(): 
    def validate_city_create(data,valid,err):
        if valid:
            if len(data['city_name'])<3:
                return Response(data={'message':"City's name can't be less than three characters",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            else :
                return Response(data={"message": "City was added successfully.",
                                      'status':Status_code.created}, 
                                    status=Status_code.created) 
        else:
            return Response(data={'message':str(err),"status":Status_code.bad_request},
                                    status=Status_code.bad_request)
            
    def validate_gov_create(data,valid,err):
        if valid:
            if len(data['gov_name'])<3:
                return Response(data={'message':"Governorate's name can't be less than three characters",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            else :
                return Response(data={"message": "Governorate was added successfully.",
                                      'status':Status_code.created}, 
                                    status=Status_code.created) 
        else:
            return Response(data={'message':str(err),"status":Status_code.bad_request},
                                    status=Status_code.bad_request)