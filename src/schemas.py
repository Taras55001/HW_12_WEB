from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr, Field

class UserModel(BaseModel):
    name: str = Field('Anon', min_length=2, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponse(UserModel):
    id: int
    surname: str = Field('Anon', min_length=2, max_length=150)
    phone: str = Field('1234567890', min_length=10, max_length=14)
    detail: str = "User successfully created"


class TokenModel(UserModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


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
