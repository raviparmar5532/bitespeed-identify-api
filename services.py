from fastapi import Depends
from sqlalchemy.orm import Session
import database, models, schemas
from sqlalchemy import or_

def get_response_from_primary_contact(primary_contact : models.Contact, db : Session) -> schemas.IdentifyResponse:

    secondary_contacts = db.query(models.Contact).filter(models.Contact.linkedId == primary_contact.id)
    emails = set([primary_contact.email])
    phoneNumbers = set([primary_contact.phoneNumber])
    secondaryContactIds = set()
    for secondary_contact in secondary_contacts:
        if secondary_contact.email: emails.add(secondary_contact.email)
        if secondary_contact.phoneNumber: phoneNumbers.add(secondary_contact.phoneNumber)
        secondaryContactIds.add(secondary_contact.id)

    return schemas.IdentifyResponse(
        primaryContactId=primary_contact.id,
        emails=list(emails),
        phoneNumbers=list(phoneNumbers),
        secondaryContactIds=list(secondaryContactIds),
    ) 



def identify_service(email:str, phoneNumber:int, db: Session) -> schemas.IdentifyResponse:

    st = set(map(lambda contact : contact.linkPrecedence.value , db.query(models.Contact)))
    if st and 'primary' not in st:
        1/0

    existing_contacts:list[models.Contact] = db.query(models.Contact).filter(
        or_(
            models.Contact.email == email,
            models.Contact.phoneNumber == phoneNumber
        )
    ).all()

    # check if contact already exists 
    already_exists = list(filter(lambda contact : contact.email == email and contact.phoneNumber == phoneNumber, existing_contacts))
    if already_exists:
        already_exists = already_exists[0]
        if already_exists.linkPrecedence == models.LinkPrecedence.secondary:
            already_exists = db.get(models.Contact, already_exists.linkedId)
        return get_response_from_primary_contact(already_exists, db)

    emails = set(map(lambda contact : contact.email, existing_contacts))
    phoneNumbers = set(map(lambda contact : contact.phoneNumber, existing_contacts))

    # if new contact 
    if email not in emails and phoneNumber not in phoneNumbers:
        new_contact = models.Contact(
            email=email,
            phoneNumber=phoneNumber,
            linkPrecedence=models.LinkPrecedence.primary,
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        return schemas.IdentifyResponse(
            primaryContactId=new_contact.id,
            emails=[email],
            phoneNumbers=[phoneNumber],
            secondaryContactIds=[]
        ) 

    # if either email or phone is present (not both)
    if email not in emails or phoneNumber not in phoneNumbers:
        primary_contacts = list(filter(lambda contact : contact.linkPrecedence == models.LinkPrecedence.primary, existing_contacts))
        for contact in existing_contacts:
            if contact.linkPrecedence == models.LinkPrecedence.secondary and (contact.email == email or contact.phoneNumber == phoneNumber):
                primary_contacts.append(db.get(models.Contact, contact.linkedId))
        
        primary_contact = min(primary_contacts, key=lambda contact: contact.createdAt)  

        new_contact = models.Contact(
            email=email,
            phoneNumber=phoneNumber,
            linkPrecedence=models.LinkPrecedence.secondary,
            linkedId=primary_contact.id
        )
        db.add(new_contact)
        db.commit()

        return get_response_from_primary_contact(primary_contact, db)

    # if email and phone both are present for two different contacts
    primary_contacts = list(filter(lambda contact : contact.linkPrecedence == models.LinkPrecedence.primary, existing_contacts))
    for contact in existing_contacts:
        if contact.linkPrecedence == models.LinkPrecedence.secondary and (contact.email == email or contact.phoneNumber == phoneNumber):
            primary_contacts.append(db.get(models.Contact, contact.linkedId))
    
    primary_contact = min(primary_contacts, key=lambda contact: contact.createdAt)

    for contact in primary_contacts:
        if contact.id != primary_contact.id:
            if contact.linkPrecedence != models.LinkPrecedence.secondary or contact.linkedId != primary_contact.id:
                contact.linkPrecedence = models.LinkPrecedence.secondary
                contact.linkedId = primary_contact.id
                db.add(contact)
    db.commit()

    return get_response_from_primary_contact(primary_contact, db)
