from pydantic import BaseModel, model_validator
from typing import Optional, Annotated
from APIExceptions import InvalidRequest, InvalidPhoneNumberException

class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None 

    @model_validator(mode='after')
    def validate_identify_request(self):
        self.email = self.email.strip()      
        self.phoneNumber = self.phoneNumber.strip()      
        
        if not self.email and not self.phoneNumber:
            raise InvalidRequest()
        if not self.phoneNumber.isnumeric():
            raise InvalidPhoneNumberException()  
        return self


class IdentifyResponse(BaseModel):
    primaryContactId: int
    emails: list[str]
    phoneNumbers: list[str]
    secondaryContactIds: list[int]
