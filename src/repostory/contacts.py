from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from src.database.models import Contact
from src.schemas import ContactResponse


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    sq = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(sq)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    sq = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(sq)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactResponse, db: AsyncSession):
    contact = Contact(name=body.name, surname=body.surname, birthday=body.birthday, phone=body.phone, email=body.email,
                      user_id=body.user_id)
    if body.description:
        contact.description = body.description
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactResponse, db: AsyncSession):
    sq = select(Contact).filter_by(id=contact_id)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.phone = body.phone
        contact.email = body.email
        contact.user_id = body.user_id
        contact.description = body.description
        await db.commit()
        await db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: AsyncSession):
    sq = select(Contact).filter_by(id=contact_id)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contact(user_id: int,
                         contact_name: str,
                         surname: str,
                         email: str,
                         db: AsyncSession):
    sq = select(Contact).filter_by(user_id=user_id)
    result = await db.execute(sq)
    query = result.scalars().all()
    con_list = []
    if contact_name:
        con_list.append(contact for contact in query if contact_name.strip().lower() in contact.name.lower())
    elif surname:
        con_list.append(contact for contact in query if surname.strip().lower() in contact.surname.lower())
    elif email:
        con_list.append(contact for contact in query if email.strip().lower() in contact.email.lower())

    return con_list[0] if len(con_list) else None


async def upcoming_birthdays(user_id, db):
    current_date = datetime.now().date()
    future_birthday = current_date + timedelta(days=7)
    sq = select(Contact).filter(Contact.user_id == user_id)
    result = await db.execute(sq)
    list_bd_contacts = result.scalars().all()
    happy_contacts = []
    for data in list_bd_contacts:
        ccy = data.birthday.replace(year=current_date.year)
        cfy = data.birthday.replace(year=future_birthday.year)
        if ccy >= current_date and cfy <= future_birthday:
            happy_contacts.append(data)
    return happy_contacts
