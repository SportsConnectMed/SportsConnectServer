from fastapi import (
    Depends,
    HTTPException,
    status,
)

from app.modules.auth.api.dependencies.get_current_user import (
    get_current_user,
)
from app.modules.users.domain.enums.user_role import UserRole
from app.modules.users.infrastructure.database.models.user_model import (
    UserModel,
)


async def require_admin_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return current_user
