from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func
from database import Base
import enum

class LinkPrecedence(str, enum.Enum):
    primary = "primary"
    secondary = "secondary"

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    phoneNumber = Column(Integer, nullable=True)
    email = Column(String(100), nullable=True)
    linkedId = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    linkPrecedence = Column(Enum(LinkPrecedence), default=LinkPrecedence.primary)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    deletedAt = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"[{self.phoneNumber} , {self.email}, {self.linkedId}]"
