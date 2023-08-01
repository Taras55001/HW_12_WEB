from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    name: str = Field('Anon', min_length=2, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponse(BaseModel):
    id: int
    surname: str | None = Field('Anon', min_length=2, max_length=150)
    phone: str | None = Field('1234567890', min_length=10, max_length=14)
    detail: str | None = "User successfully created"

    class Config:
        from_attributes = True

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactModel(BaseModel):
    name: str | None = Field('Anon', min_length=2, max_length=150)
    surname: str | None = Field('Anon', min_length=2, max_length=150)
    description: Optional[str] = Field(None)
    birthday: date | None
    phone: str | None = Field('1234567890', min_length=10, max_length=14)
    email: EmailStr | None
    user_id: UserResponse


class ContactResponse(BaseModel):
    id: int
    description: str | None
    class Config:
        from_attributes = True
