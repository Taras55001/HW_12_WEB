from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas import UserResponse, UserModel


async def get_users(limit: int, offset: int, db: AsyncSession):
    sq = select(User).offset(offset).limit(limit)
    users = await db.execute(sq)
    return users.scalars().all()


async def get_user(user_id: int, db: AsyncSession):
    sq = select(User).filter_by(id=user_id)
    users = await db.execute(sq)
    return users.scalar_one_or_none()


async def get_user_by_email(email: str, db: AsyncSession):
    sq = select(User).filter_by(email=email)
    result = await db.execute(sq)
    user = result.scalar_one_or_none()
    return user


async def create_user(body: UserModel, db: AsyncSession):
    user = User(**body.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(user_id: int, body: UserResponse, db: AsyncSession):
    sq = select(User).filter_by(id=user_id)
    result = await db.execute(sq)
    user = result.scalar_one_or_none()
    if user:
        user.name = body.name
        user.surname = body.surname
        user.phone = body.phone
        user.email = body.email
        await db.commit()
        await db.refresh(user)
    return user


async def remove_user(user_id: int, db: AsyncSession):
    sq = select(User).filter_by(id=user_id)
    result = await db.execute(sq)
    user = result.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()
    return user
