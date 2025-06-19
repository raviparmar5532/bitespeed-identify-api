from pydantic import BaseModel
from typing import Optional

class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None

class IdentifyResponse(BaseModel):
    primaryContactId: int
    emails: list[str]
    phoneNumbers: list[str]
    secondaryContactIds: list[int]
