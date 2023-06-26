from rest_framework.response import Response
from rest_framework import status
import re


class PlaygroundAppValidations():
    
    def validate_playground_create(data,valid,err):
        h_m_s_regex="^(((([0-1][0-9])|(2[0-3])):?[0-5][0-9]:?[0-5][0-9]+$))"

        if valid:
            if len(data['p_name']) < 3:
                return Response(data={'message': "Playground's name can't be less than three characters",
                                      'status':status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            if not re.match(h_m_s_regex,data['open_time']):
                return Response(data={'message': "Playground's open_time doesn't match time H:M:S format",
                                      'status':status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            if not re.match(h_m_s_regex,data['close_time']):
                return Response(data={'message': "Playground's close_time doesn't match time H:M:S format",
                                      'status':status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            if len(data['description']) < 10:
                return Response(data={'message': "Playground's description can't be less than 10 characters",
                                      'status':status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            if float(data['price_per_hour']) < 10.0:
                return Response(data={'message': "Playground's price can't be less than 10 pounds",
                                      'status':status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"message": "Playground was added successfully.",
                                      'status':status.HTTP_201_CREATED},
                                status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message':str(err),"status":status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
    
    def validate_playground_update(data,valid,err):
        if valid:
            #this regex to make sure user inputs the right time format
            h_m_s_regex="^(((([0-1][0-9])|(2[0-3])):?[0-5][0-9]:?[0-5][0-9]+$))"

            # if ('city'or'governorate') in data.keys():
            #     return Response(data={'message': "No Authorization to update city",
            #                             'status':status.HTTP_401_UNAUTHORIZED },
            #                     status=status.HTTP_401_UNAUTHORIZED)
            
            if 'p_name' in data.keys():
                if len(data['p_name'])!=0 and len(data['p_name'])< 3:
                    return Response(data={'message': "Playground's name can't be less than three characters",
                                            'status':status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            if 'open_time' in data.keys():      
                if not re.match(h_m_s_regex,data['open_time']):
                    return Response(data={'message': "Playground's open_time doesn't match time H:M:S format",
                                            'status':status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            if 'close_time' in data.keys():
                if not re.match(h_m_s_regex,data['close_time']):
                    return Response(data={'message': "Playground's close_time doesn't match time H:M:S format",
                                            'status':status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            if 'description' in data.keys():
                if len(data['description']) < 10:
                    return Response(data={'message': "Playground's description can't be less than 10 characters",
                                            'status':status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            if 'price_per_hour' in data.keys():       
                if float(data['price_per_hour']) < 10.0:
                    return Response(data={'message': "Playground's price can't be less than 10 pounds",
                                            'status':status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            
            return Response(data={"message": "Playground was updated successfully.",
                                    'status':status.HTTP_202_ACCEPTED},
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data={'message':str(err),"status":status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)