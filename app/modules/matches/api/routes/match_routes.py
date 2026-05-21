from fastapi import APIRouter, Depends, HTTPException, status
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
from app.modules.matches.use_cases.get_match_by_id_use_case import GetMatchByIdUseCase
from app.modules.matches.use_cases.get_matches_use_case import GetMatchesUseCase
from app.modules.matches.use_cases.join_match_use_case import JoinMatchUseCase
from app.modules.matches.use_cases.kick_player_use_case import KickPlayerUseCase
from app.modules.matches.use_cases.leave_match_use_case import LeaveMatchUseCase
from app.modules.users.infrastructure.database.models.user_model import (
    UserModel,
)

router = APIRouter(
    prefix="/matches",
    tags=["Matches"],
)


@router.get(
    "",
    response_model=list[MatchResponseSchema],
)
async def get_matches(
    db: AsyncSession = Depends(get_db), _: UserModel = Depends(get_current_user)
):

    repository = SQLAlchemyMatchRepository(db)

    use_case = GetMatchesUseCase(repository)

    matches = await use_case.execute()

    return [MatchResponseSchema.model_validate(match) for match in matches]


@router.get(
    "/{match_id}",
    response_model=MatchResponseSchema,
)
async def get_match(
    match_id: str,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(get_current_user),
):

    repository = SQLAlchemyMatchRepository(db)

    use_case = GetMatchByIdUseCase(repository)

    match = await use_case.execute(match_id)

    return MatchResponseSchema.model_validate(match)


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


@router.delete(
    "/{match_id}/players/{user_id}",
    response_model=MatchResponseSchema,
)
async def kick_player(
    match_id: str,
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    match_repository = SQLAlchemyMatchRepository(db)

    match_player_repository = SQLAlchemyMatchPlayerRepository(db)

    use_case = KickPlayerUseCase(
        db=db,
        match_repository=match_repository,
        match_player_repository=match_player_repository,
    )

    try:
        match = await use_case.execute(
            match_id=match_id,
            owner_id=current_user.id,
            kicked_user_id=user_id,
        )

        return MatchResponseSchema.model_validate(match)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
