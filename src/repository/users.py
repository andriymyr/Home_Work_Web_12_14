from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    Get a user by email.

    :param email: str: Email of the user to retrieve.
    :param db: AsyncSession: Database connection to use (Dependency).
    :return: User object or None if not found.
    """    
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    Create a new user.

    :param body: UserSchema: User data to create.
    :param db: AsyncSession: Database connection to use (Dependency).
    :return: Created User object.
    """    
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    Update the refresh token for a user.

    :param user: User: User object to update.
    :param token: str | None: New refresh token value.
    :param db: AsyncSession: Database connection to use.
    :return: None
    """    
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Confirm the email for a user.

    :param email: str: Email to confirm.
    :param db: AsyncSession: Database connection to use.
    :return: None
    """    
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    Update the avatar URL for a user.

    :param email: str: Email of the user to update.
    :param url: str | None: New avatar URL.
    :param db: AsyncSession: Database connection to use.
    :return: Updated User object.
    """  
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
