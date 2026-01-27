import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security
import uuid


async def get_user_by_username(db:AsyncSession, username:str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalars().one_or_none()


async def create_user(db:AsyncSession, user_data:UserRequest):
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user



async def create_token(db:AsyncSession,user_id:int):
    token = str(uuid.uuid4())
    expires_at= datetime.datetime.now() + datetime.timedelta(days=7)
    query=select(UserToken).where(UserToken.user_id == user_id)
    result=await db.execute(query)
    user_token=result.scalars().one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token


async def authenticate_user(db:AsyncSession, username:str, password:str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None

    return user


async def get_user_by_token(db:AsyncSession, token:str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalars().one_or_none()
    if not db_token or db_token.expires_at < datetime.datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalars().one_or_none()
