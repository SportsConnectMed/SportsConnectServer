from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.auth.api.dependencies.get_current_user import get_current_user
from app.modules.auth.api.dependencies.require_admin_user import require_admin_user
from app.modules.auth.api.dependencies.require_same_user_or_admin import (
    require_same_user_or_admin,
)
from app.modules.users.api.dependencies.user_dependencies import (
    get_user_repository,
)
from app.modules.users.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from app.modules.users.application.use_cases.delete_user_use_case import (
    DeleteUserUseCase,
)
from app.modules.users.application.use_cases.get_user_by_id_use_case import (
    GetUserByIDUseCase,
)
from app.modules.users.application.use_cases.get_users_use_case import (
    GetUsersUserUseCase,
)
from app.modules.users.application.use_cases.update_user_use_case import (
    UpdateUserUseCase,
)
from app.modules.users.infrastructure.database.models.user_model import UserModel
from app.modules.users.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.modules.users.schemas.message_response_schema import MessageResponseSchema
from app.modules.users.schemas.user_create_schema import (
    UserCreateSchema,
)
from app.modules.users.schemas.user_response_schema import (
    UserResponseSchema,
)
from app.modules.users.schemas.user_update_schema import UserUpdateSchema
from app.modules.users.schemas.users_list_response_schema import UserListResponseSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=UserListResponseSchema,
)
async def get_users(
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    _: UserModel = Depends(require_admin_user),
):
    use_case = GetUsersUserUseCase(user_repository)

    users = await use_case.execute()

    return UserListResponseSchema(
        total=len(users),
        active=len([u for u in users if u.is_active]),
        inactive=len([u for u in users if not u.is_active]),
        users=[
            UserResponseSchema.model_validate(user) for user in users if user.is_active
        ],
    )


@router.get(
    "/me",
    response_model=UserResponseSchema,
)
async def get_user_me(
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    current_user: UserModel = Depends(get_current_user),
):
    use_case = GetUserByIDUseCase(user_repository, current_user.id)

    user = await use_case.execute()

    return UserResponseSchema.model_validate(user)


@router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
)
async def get_user_by_id(
    user_id: str,
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    _: UserModel = Depends(require_admin_user),
):
    use_case = GetUserByIDUseCase(user_repository, user_id)

    user = await use_case.execute()

    return UserResponseSchema.model_validate(user)


@router.post(
    "",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserCreateSchema,
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
):
    use_case = CreateUserUseCase(user_repository)

    try:
        user = await use_case.execute(data)

        return UserResponseSchema.model_validate(user)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.patch(
    "/{user_id}", response_model=UserResponseSchema, status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: str,
    data: UserUpdateSchema,
    user_respository: SQLAlchemyUserRepository = Depends(get_user_repository),
    _: UserModel = Depends(require_same_user_or_admin),
):
    use_case = UpdateUserUseCase(user_respository, user_id, update_data=data)

    try:
        user = await use_case.execute()

        return UserResponseSchema.model_validate(user)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.delete(
    "/{user_id}", response_model=MessageResponseSchema, status_code=status.HTTP_200_OK
)
async def delete_user(
    user_id: str,
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
    _: UserModel = Depends(require_same_user_or_admin),
):
    use_case = DeleteUserUseCase(user_repository, user_id)

    try:
        await use_case.execute()

        return MessageResponseSchema(message="User deleted succesfully")

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
