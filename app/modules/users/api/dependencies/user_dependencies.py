from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.users.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


async def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)
