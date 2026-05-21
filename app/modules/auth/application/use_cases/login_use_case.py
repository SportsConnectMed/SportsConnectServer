from app.core.security import (
    create_access_token,
    verify_password,
)
from app.modules.auth.schemas.login_schema import (
    LoginSchema,
)
from app.modules.auth.schemas.token_schema import (
    TokenSchema,
)
from app.modules.users.domain.repositories.user_repository import (
    UserRepository,
)


class LoginUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def execute(
        self,
        data: LoginSchema,
    ) -> TokenSchema:
        user = await self.user_repository.get_by_email(data.email)

        if not user:
            raise ValueError("Invalid credentials")

        is_valid_password = verify_password(
            data.password,
            user.hashed_password,
        )

        if not is_valid_password:
            raise ValueError("Invalid credentials")

        access_token = create_access_token(subject=user.id)

        return TokenSchema(
            access_token=access_token,
        )
