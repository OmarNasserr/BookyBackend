from rest_framework.response import Response
from rest_framework import status
import re
from helper_files.status_code import Status_code


class PlaygroundAppValidations():
    
    def validate_playground_create(data,valid,err):
        h_m_s_regex="^(((([0-1][0-9])|(2[0-3])):?[0-5][0-9]:?[0-5][0-9]+$))"

        if valid:
            if len(data['p_name']) < 3:
                return Response(data={'message': "Playground's name can't be less than three characters",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            if not re.match(h_m_s_regex,data['open_time']):
                return Response(data={'message': "Playground's open_time doesn't match time H:M:S format",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            if not re.match(h_m_s_regex,data['close_time']):
                return Response(data={'message': "Playground's close_time doesn't match time H:M:S format",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            if len(data['description']) < 10:
                return Response(data={'message': "Playground's description can't be less than 10 characters",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            if float(data['price_per_hour']) < 10.0:
                return Response(data={'message': "Playground's price can't be less than 10 pounds",
                                      'status':Status_code.bad_request},
                                status=Status_code.bad_request)
            else:
                return Response(data={"message": "Playground was added successfully.",
                                      'status':Status_code.created},
                                status=Status_code.created)
        else:
            return Response(data={'message':str(err),"status":Status_code.bad_request},
                                    status=Status_code.bad_request)
    
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
                                            'status':Status_code.bad_request},
                                    status=Status_code.bad_request)
            if 'open_time' in data.keys():      
                if not re.match(h_m_s_regex,data['open_time']):
                    return Response(data={'message': "Playground's open_time doesn't match time H:M:S format",
                                            'status':Status_code.bad_request},
                                    status=Status_code.bad_request)
            if 'close_time' in data.keys():
                if not re.match(h_m_s_regex,data['close_time']):
                    return Response(data={'message': "Playground's close_time doesn't match time H:M:S format",
                                            'status':Status_code.bad_request},
                                    status=Status_code.bad_request)
            if 'description' in data.keys():
                if len(data['description']) < 10:
                    return Response(data={'message': "Playground's description can't be less than 10 characters",
                                            'status':Status_code.bad_request},
                                    status=Status_code.bad_request)
            if 'price_per_hour' in data.keys():       
                if float(data['price_per_hour']) < 10.0:
                    return Response(data={'message': "Playground's price can't be less than 10 pounds",
                                            'status':Status_code.bad_request},
                                    status=Status_code.bad_request)
            
            return Response(data={"message": "Playground was updated successfully.",
                                    'status':Status_code.updated},
                            status=Status_code.updated)
        else:
            return Response(data={'message':str(err),"status":Status_code.bad_request},
                                    status=Status_code.bad_request)