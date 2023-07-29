from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    name: str = Field('Anon', min_length=2, max_length=150)
    surname: str = Field('Anon', min_length=2, max_length=150)
    phone: str = Field('1234567890', min_length=10, max_length=14)
    email: EmailStr


class UserResponse(UserModel):
    id: int


class ContactModel(BaseModel):
    name: str = Field('Anon', min_length=2, max_length=150)
    surname: str = Field('Anon', min_length=2, max_length=150)
    description: Optional[str] = Field(None)
    birthday: date
    phone: str = Field('1234567890', min_length=10, max_length=14)
    email: EmailStr
    user_id: int = Field(1)

class ContactResponse(ContactModel):
    id: int
