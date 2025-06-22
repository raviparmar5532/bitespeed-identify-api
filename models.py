from sqlalchemy import Column, Integer, String, Enum, ForeignKey, func
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.orm import validates
from database import Base
import enum
import datetime

class LinkPrecedence(str, enum.Enum):
    primary = "primary"
    secondary = "secondary"

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    phoneNumber = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    linkedId = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    linkPrecedence = Column(Enum(LinkPrecedence), default=LinkPrecedence.primary)
    createdAt = Column(TIMESTAMP(fsp=6), default=datetime.datetime.now)
    updatedAt = Column(TIMESTAMP(fsp=6), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    deletedAt = Column(TIMESTAMP(fsp=6), nullable=True)

    def __repr__(self):
        return f"[{self.phoneNumber} , {self.email}, {self.linkedId}]"
