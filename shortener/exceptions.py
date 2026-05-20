from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that wraps all DRF errors
    in a consistent JSON structure.

    Registered in settings.py under REST_FRAMEWORK.
    """

    # Call DRF's default handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Wrap the default error response in our standard structure
        response.data = {
            "success": False,
            "status_code": response.status_code,
            "error": response.data
        }

    return response