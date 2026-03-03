
class ApplicationException(Exception):


    def __init__(self, message="No Message", error=None):
        self.message= message
        self.error = error
        super().__init__(message)



