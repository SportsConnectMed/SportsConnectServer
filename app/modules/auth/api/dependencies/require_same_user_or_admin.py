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


async def require_same_user_or_admin(
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:

    if current_user.role == UserRole.ADMIN:
        return current_user

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return current_user
