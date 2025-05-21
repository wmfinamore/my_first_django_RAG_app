from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.views import exception_handler


def customexception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, NotFound):
            response.data = {'error': 'The requested resource was not found'}
        elif isinstance(exc, MethodNotAllowed):
            response.data = {'error': f'The {exc.method} method is not allowed for this resource'}
    return response
