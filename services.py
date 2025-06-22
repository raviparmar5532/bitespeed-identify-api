from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import or_

def get_response_from_primary_contact(primary_contact : models.Contact, db : Session) -> schemas.IdentifyResponse:

    secondary_contacts = db.query(models.Contact).filter(models.Contact.linkedId == primary_contact.id)

    emails = set([primary_contact.email] if primary_contact.email else [])
    phoneNumbers = set([primary_contact.phoneNumber] if primary_contact.phoneNumber else [])

    secondaryContactIds = set()

    for secondary_contact in secondary_contacts:
        if secondary_contact.email: emails.add(secondary_contact.email)
        if secondary_contact.phoneNumber: phoneNumbers.add(secondary_contact.phoneNumber)
        secondaryContactIds.add(secondary_contact.id)

    return schemas.IdentifyResponse(
        primaryContactId = primary_contact.id,
        emails = list(emails),
        phoneNumbers = list(phoneNumbers),
        secondaryContactIds = list(secondaryContactIds),
    ) 

def change_secondary_contacts_parent_to_primary_contact(primary_contact : models.Contact, id : int, db : Session):

    secondary_contacts = db.query(models.Contact).filter(models.Contact.linkedId == primary_contact.id).all()

    for secondary_contact in secondary_contacts:
        if secondary_contact.linkedId != id:
            secondary_contact.linkedId = id
            db.add(secondary_contact)
        change_secondary_contacts_parent_to_primary_contact(secondary_contact, id, db)
    db.commit()

async def identify_service(email:str, phoneNumber:str, db: Session) -> schemas.IdentifyResponse:

    same_contacts:list[models.Contact] = db.query(models.Contact).filter(
        or_(
            (email and models.Contact.email == email),
            (phoneNumber and models.Contact.phoneNumber == phoneNumber)
        )
    ).all()

    # check if contact already exists 
    if email and phoneNumber:
        already_exists = list(filter(lambda contact : contact.email == email and contact.phoneNumber == phoneNumber, same_contacts))
    elif email:
        already_exists = list(filter(lambda contact : contact.email == email, same_contacts))
    elif phoneNumber:
        already_exists = list(filter(lambda contact : contact.phoneNumber == phoneNumber, same_contacts))

    if already_exists:
        already_exists = already_exists[0]
        if already_exists.linkPrecedence == models.LinkPrecedence.secondary:
            already_exists = db.get(models.Contact, already_exists.linkedId)
        return get_response_from_primary_contact(already_exists, db)

    emails = set(filter(bool, map(lambda contact : contact.email, same_contacts)))
    phoneNumbers = set(filter(bool, map(lambda contact : contact.phoneNumber, same_contacts)))

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
            emails=[email] if email else [],
            phoneNumbers=[phoneNumber] if phoneNumber else [],
            secondaryContactIds=[]
        ) 

    # if either email or phone is present (not both)
    if (email and email not in emails) or (phoneNumber and phoneNumber not in phoneNumbers):
        primary_contacts = list(filter(lambda contact : contact.linkPrecedence == models.LinkPrecedence.primary, same_contacts))
        for contact in same_contacts:
            if contact.linkPrecedence == models.LinkPrecedence.secondary and ((email and contact.email == email) or (phoneNumber and contact.phoneNumber == phoneNumber)):
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
    primary_contacts = list(filter(lambda contact : contact.linkPrecedence == models.LinkPrecedence.primary, same_contacts))
    for contact in same_contacts:
        if contact.linkPrecedence == models.LinkPrecedence.secondary and (contact.email == email or contact.phoneNumber == phoneNumber):
            primary_contacts.append(db.get(models.Contact, contact.linkedId))
    
    primary_contact = min(primary_contacts, key=lambda contact: contact.createdAt)

    for contact in primary_contacts:
        if contact.id != primary_contact.id:
            contact.linkedId = primary_contact.id
            contact.linkPrecedence = models.LinkPrecedence.secondary
            db.add(contact)
    db.commit()

    change_secondary_contacts_parent_to_primary_contact(primary_contact, primary_contact.id, db)

    return get_response_from_primary_contact(primary_contact, db)



def truncate_database(db: Session):
    for contact in db.query(models.Contact).all():
        db.delete(contact)
    db.commit()
