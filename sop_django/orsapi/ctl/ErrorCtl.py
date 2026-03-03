# ctl/ErrorCtl.py
from django.http import JsonResponse
from django.db.utils import OperationalError
from ..utility.ApplicationException import ApplicationException

class ErrorCtl:

    @staticmethod
    def handle(ex):
        print(">>>>>>>>>inside ErrorCtl handle method")

        # Database connection errors
        if isinstance(ex, OperationalError):
            message = "Database service is currently unavailable. Please try again later!!!!!."
            print(">>>>>>>>>>>>>>>",message)
            status_code = 500

        # Custom application-level errors
        elif isinstance(ex, ApplicationException):
            message = ex.message
            print("##########",message)
            status_code = 500

        # All other unexpected exceptions
        else:
            message = str(ex)
            print("_____________",message)
            status_code = 500

        return JsonResponse(
            {
                "success": False,
                "result": {
                    "message": message
                }
            },
            status=status_code
        )