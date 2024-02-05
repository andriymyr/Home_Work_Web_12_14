import pickle

import cloudinary
import cloudinary.uploader
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Path,
    Query,
    UploadFile,
    File,
)
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserResponse
from src.services.auth import auth_service
from src.database.db import CLD_NAME, CLD_API_KEY,CLD_API_SECRET
from src.repository import users as repositories_users

router = APIRouter(prefix="/users", tags=["users"])
cloudinary.config(
    cloud_name=CLD_NAME,
    api_key=CLD_API_KEY,
    api_secret=CLD_API_SECRET,
    secure=True,
)


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    """
    Get the details of the currently authenticated user.

    :param user: User: Authenticated user.
    :return: User details.
    """
    return user


@router.patch(
    "/avatar",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def get_current_user(
    file: UploadFile = File(),
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update the avatar of the currently authenticated user.

    :param file: UploadFile: Avatar file to upload.
    :param user: User: Authenticated user.
    :param db: AsyncSession: Database session.
    :return: Updated user details with the new avatar.
    """
    public_id = f"Web16/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    print(res)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    user = await repositories_users.update_avatar_url(user.email, res_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)
    return user
