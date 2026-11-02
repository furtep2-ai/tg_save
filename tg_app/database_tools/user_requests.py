from tg_app.database_tools.database import AsyncSessionLocal, User
from sqlalchemy import delete, insert, select
import asyncio


async def select_user(user_id: int):
    async with AsyncSessionLocal() as session:
        query = select(User).where(User.user_id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
    return user if user else None

async def create_user(user_id: int, user_name: str, is_admin: bool):
    async with AsyncSessionLocal() as session:
        query = insert(User).values(
        user_id=user_id,
        user_name=user_name,
        is_admin=is_admin)
        result = await session.execute(query)
        await session.commit()
        return True if result.rowcount>0 else False

async def delete_user(user_id: int):
    async with AsyncSessionLocal() as session:
        query = delete(User).where(User.user_id == user_id)
        result = await session.execute(query)
        await session.commit()
        return True if result.rowcount>0 else False

async def list_users():
    async with AsyncSessionLocal() as session:
        query = select(User)
        result = await session.execute(query)
        users = result.scalars().all()
        return users if users else False

async def make_admin(user_id: int):
    async with AsyncSessionLocal() as session:
        query = select(User).where(User.user_id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return "error"

        if user.is_admin:
            return "Already admin"
            
        user.is_admin = True
        await session.commit()
        await session.refresh(user)
        return "success"

async def delete_admin(user_id: int):
    async with AsyncSessionLocal() as session:
        query = select(User).where(User.user_id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return "error"

        if not user.is_admin:
            return "Already user"

        user.is_admin = False
        await session.commit()
        await session.refresh(user)
        return "success"

async def save_user(user_id: int, user_name: str, timezone: str):
    async with AsyncSessionLocal() as session:
        new_user = User(user_id = user_id, user_name = user_name)
        session.add(new_user)
        await session.commit()
    return True


async def select_timezone(user_id: int) -> str | None:
    async with AsyncSessionLocal() as session:
        query = select(User.time_zone).where(User.user_id == user_id)
        result = await session.execute(query)
        timezone = result.scalar_one_or_none()
    return timezone