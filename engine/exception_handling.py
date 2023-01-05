import copy
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        key = list(response.data.keys())[0]
        value = response.data[list(response.data.keys())[0]]
        data = dict({
            "error": "{0} - {1}".format(key, value[0]) if isinstance(value, list) else "{0} - {1}".format(key, value)
        })
        response.data = copy.deepcopy(data)
    return response