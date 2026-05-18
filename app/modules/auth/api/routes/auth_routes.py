from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.modules.auth.application.use_cases.login_use_case import (
    LoginUseCase,
)
from app.modules.auth.schemas.login_schema import (
    LoginSchema,
)
from app.modules.auth.schemas.token_schema import (
    TokenSchema,
)
from app.modules.users.api.dependencies.user_dependencies import (
    get_user_repository,
)
from app.modules.users.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    response_model=TokenSchema,
)
async def login(
    data: LoginSchema,
    user_repository: SQLAlchemyUserRepository = Depends(get_user_repository),
):
    use_case = LoginUseCase(user_repository)

    try:
        return await use_case.execute(data)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )
