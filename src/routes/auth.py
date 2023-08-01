from typing import List

from fastapi import APIRouter, HTTPException, Depends, Path, Query, status

from src.database.db import get_db
from src.schemas import UserResponse, UserModel, TokenModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository import users as repository_users
from src.services.auth import oauth2_scheme, auth_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def get_user(body=UserModel, db: AsyncSession = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exist")
    body.password = auth_service.password_manager.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    return new_user


@router.post("/login", response_model=TokenModel, status_code=status.HTTP_200_OK)
async def login_user(body=UserModel, db: AsyncSession = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not auth_service.password_manager.verify_password(body.password, exist_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    access_toke = await auth_service.create_access_token(exist_user)
    refresh_token = await auth_service.create_refresh_token(exist_user)
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}
