from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth.api.dependencies.get_current_user import (
    get_current_user,
)
from app.modules.matches.infrastructure.repositories.sqlalchemy_match_player_repository import (
    SQLAlchemyMatchPlayerRepository,
)
from app.modules.matches.infrastructure.repositories.sqlalchemy_match_repository import (
    SQLAlchemyMatchRepository,
)
from app.modules.matches.schemas.match_create_schema import (
    MatchCreateSchema,
)
from app.modules.matches.schemas.match_response_schema import MatchResponseSchema
from app.modules.matches.use_cases.cancel_match_use_case import CancelMatchUseCase
from app.modules.matches.use_cases.create_match_use_case import (
    CreateMatchUseCase,
)
from app.modules.matches.use_cases.join_match_use_case import JoinMatchUseCase
from app.modules.matches.use_cases.leave_match_use_case import LeaveMatchUseCase
from app.modules.users.infrastructure.database.models.user_model import (
    UserModel,
)

router = APIRouter(
    prefix="/matches",
    tags=["Matches"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_match(
    data: MatchCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    match_repository = SQLAlchemyMatchRepository(db)

    match_player_repository = SQLAlchemyMatchPlayerRepository(db)

    use_case = CreateMatchUseCase(
        db=db,
        match_repository=match_repository,
        match_player_repository=match_player_repository,
    )

    return await use_case.execute(
        data=data,
        creator_id=current_user.id,
    )


@router.post(
    "/{match_id}/join",
    status_code=status.HTTP_200_OK,
    response_model=MatchResponseSchema,
)
async def join_match(
    match_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    match_repository = SQLAlchemyMatchRepository(db)

    match_player_repository = SQLAlchemyMatchPlayerRepository(db)

    use_case = JoinMatchUseCase(
        db=db,
        match_repository=match_repository,
        match_player_repository=match_player_repository,
    )

    match = await use_case.execute(
        match_id=match_id,
        user_id=current_user.id,
    )

    return MatchResponseSchema.model_validate(match)


@router.post(
    "/{match_id}/leave",
    status_code=status.HTTP_200_OK,
    response_model=MatchResponseSchema,
)
async def leave_match(
    match_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    match_repository = SQLAlchemyMatchRepository(db)

    match_player_repository = SQLAlchemyMatchPlayerRepository(db)

    use_case = LeaveMatchUseCase(
        db=db,
        match_repository=match_repository,
        match_player_repository=match_player_repository,
    )

    match = await use_case.execute(
        match_id=match_id,
        user_id=current_user.id,
    )

    return MatchResponseSchema.model_validate(match)


@router.post(
    "/{match_id}/cancel",
    status_code=status.HTTP_200_OK,
    response_model=MatchResponseSchema,
)
async def cancel_match(
    match_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    match_repository = SQLAlchemyMatchRepository(db)

    use_case = CancelMatchUseCase(
        db=db,
        match_repository=match_repository,
    )

    match = await use_case.execute(
        match_id=match_id,
        user_id=current_user.id,
    )

    return MatchResponseSchema.model_validate(match)
