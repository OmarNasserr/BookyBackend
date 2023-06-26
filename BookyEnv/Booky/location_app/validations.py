from rest_framework.response import Response
from rest_framework import status

class LocationAppValidations(): 
    def validate_city_create(data,valid,err):
        if valid:
            if len(data['city_name'])<3:
                return Response(data={'message':"City's name can't be less than three characters",
                                      'status':status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            else :
                return Response(data={"message": "City was added successfully.",
                                      'status':status.HTTP_201_CREATED}, 
                                    status=status.HTTP_201_CREATED) 
        else:
            return Response(data={'message':str(err),"status":status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            
    def validate_gov_create(data,valid,err):
        if valid:
            if len(data['gov_name'])<3:
                return Response(data={'message':"Governorate's name can't be less than three characters",
                                      'status':status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            else :
                return Response(data={"message": "Governorate was added successfully.",
                                      'status':status.HTTP_201_CREATED}, 
                                    status=status.HTTP_201_CREATED) 
        else:
            return Response(data={'message':str(err),"status":status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)