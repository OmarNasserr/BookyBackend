from rest_framework.response import Response
from helper_files.status_code import Status_code

class GeneralValidations():
    def displayErrMessage(err):
        dictt = dict(err.detail)
        key = list(dictt.keys())[0]
        error_message = str(dictt[key][0])
        return Response(data={
            'message': "'" + key + "'" + " " + error_message,
            'status': Status_code.bad_request},
            status=Status_code.bad_request)