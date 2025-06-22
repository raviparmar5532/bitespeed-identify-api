from pydantic import BaseModel, model_validator
from typing import Optional
from exceptions import InvalidRequest, InvalidPhoneNumberException, InvalidEmailException

class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None 

    @model_validator(mode='after')
    def validate_identify_request(self):
        if self.email is not None: self.email = self.email.strip()      
        if self.phoneNumber is not None: self.phoneNumber = self.phoneNumber.strip()      
        
        if not self.email and not self.phoneNumber:
            raise InvalidRequest()
        if self.email == "" or self.phoneNumber == "":
            raise InvalidRequest()
        if self.phoneNumber and not self.phoneNumber.isnumeric():
            raise InvalidPhoneNumberException()  
        if self.phoneNumber and len(self.phoneNumber) > 20:
            raise InvalidPhoneNumberException("Phone number is too long")  
        if self.email and len(self.email) > 100:
            raise InvalidEmailException("Email is too long")  
        return self


class IdentifyResponse(BaseModel):
    primaryContactId: int
    emails: list[str]
    phoneNumbers: list[str]
    secondaryContactIds: list[int]
