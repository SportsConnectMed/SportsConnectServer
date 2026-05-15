from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.users.api.dependencies.user_dependencies import (
    get_user_repository,
)
from app.modules.users.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from app.modules.users.application.use_cases.get_users_use_case import (
    GetUsersUserUseCase,
)
from app.modules.users.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.modules.users.schemas.user_create_schema import (
    UserCreateSchema,
)
from app.modules.users.schemas.user_response_schema import (
    UserResponseSchema,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserResponseSchema],
)
async def get_users(
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
):
    use_case = GetUsersUserUseCase(user_repository)

    users = await use_case.execute()

    return [UserResponseSchema.model_validate(user) for user in users]


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
