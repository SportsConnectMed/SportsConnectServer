from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.database import get_db
from app.core.security import (
    decode_access_token,
)
from app.modules.users.infrastructure.database.models.user_model import (
    UserModel,
)
from app.modules.users.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)

from .auth_dependencies import oauth2_scheme


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

        repository = SQLAlchemyUserRepository(db)

        user = await repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        return user

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
