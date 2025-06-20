from fastapi import HTTPException, status

class APIException(HTTPException):
    def __init__(self, message, code):
        super().__init__(status_code=code, detail=message)

class InvalidPhoneNumberException(APIException):
    def __init__(self, message="Invalid Phone Number", code=status.HTTP_400_BAD_REQUEST):
        super().__init__(message, code)

class InvalidRequest(APIException):
    def __init__(self, message="Invalid Email or Phone number", code = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, code)