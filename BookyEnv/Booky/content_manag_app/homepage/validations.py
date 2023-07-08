from rest_framework.response import Response
from rest_framework import status
import re
from helper_files.status_code import Status_code


class HomaPageValidations():

    def validate_slider_image_create(data, valid, err, create=True):

        accepted_extensions = ['.jpg', '.jpeg', ]
        if valid:
            if 'image' in data:
                if len(str(data['image']).lower()) == 0:
                    return Response(data={
                        'message': "'image' field can't be null",
                        'status': Status_code.bad_request},
                        status=Status_code.bad_request)
                elif not any(str(data['image']).lower().endswith(ext) for ext in accepted_extensions):
                    return Response(data={
                        'message': "Invalid file extension. Only images with extensions: {} are allowed.".format(
                            accepted_extensions),
                        'status': Status_code.bad_request},
                        status=Status_code.bad_request)
                else:
                    return Response(data={
                        "message": "Slider image was added successfully." if create else "Slider image was updated "
                                                                                         "successfully.",
                        'status': Status_code.created if create else Status_code.updated},
                                    status=Status_code.created if create else Status_code.updated)
            else:
                return Response(data={
                    'message': "'image' field is required",
                    'status': Status_code.bad_request},
                    status=Status_code.bad_request)
        else:
            return Response(data={'message': str(err), "status": Status_code.bad_request},
                            status=Status_code.bad_request)
