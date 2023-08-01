import os
from typing import Dict, Any, Optional

from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository import users as repository_users



class PasswordManager:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


class JWTManager:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, data: Dict[str, Any], expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        encoded_token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_token

    def decode_token(self, token: str):
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            return None


class AuthService:
    def __init__(self, password_manager, jwt_manager, user_repository):
        self.password_manager = password_manager
        self.jwt_manager = jwt_manager
        self.user_repository = user_repository

    async def authenticate_user(self, email: str, password: str, db: AsyncSession):
        user = await self.user_repository.get_user_by_email(email, db)
        if user is None or not self.password_manager.verify_password(password, user.pasword):
            return None
        return user

    async def authorised_user(self, token: str, db: AsyncSession):
        try:
            peyload = self.jwt_manager.decode_token(token)
            if peyload["scope"] == "access_token":
                email = peyload["sub"]
                if email is None:
                    return None
            else:
                return None
        except JWTError:
            return None
        user = await self.user_repository.get_user_by_email(email, db)
        if user is None:
            return None
        return user

    async def create_access_token(self, user):
        access_token_expires = 900
        access_token_data = {"sub": user.email}
        return self.jwt_manager.create_token(access_token_data, access_token_expires)

    async def create_refresh_token(self, user):
        refresh_token_expires = 604800
        refresh_token_data = {"sub": user.email}
        return self.jwt_manager.create_token(refresh_token_data, refresh_token_expires)


load_dotenv()
secret_key = os.getenv("PASSWORD")
algorithm = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
auth_service = AuthService(PasswordManager(), JWTManager(secret_key, algorithm), repository_users)
