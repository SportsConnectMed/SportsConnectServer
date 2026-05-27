from datetime import date
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums.skill_level import SkillLevel
from app.common.enums.sport_type import SportType
from app.core.database import get_db
from app.modules.auth.api.dependencies.get_current_user import (
    get_current_user,
)
from app.modules.matches.domain.enums.match_status import MatchStatus
from app.modules.matches.infrastructure.repositories.sqlalchemy_match_player_repository import (
    SQLAlchemyMatchPlayerRepository,
)
from app.modules.matches.infrastructure.repositories.sqlalchemy_match_repository import (
    SQLAlchemyMatchRepository,
)
from app.modules.matches.schemas.match_create_schema import (
    MatchCreateSchema,
)
from app.modules.matches.schemas.match_list_response_schema import (
    MatchListResponseSchema,
)
from app.modules.matches.schemas.match_response_schema import MatchResponseSchema
from app.modules.matches.use_cases.cancel_match_use_case import CancelMatchUseCase
from app.modules.matches.use_cases.create_match_use_case import (
    CreateMatchUseCase,
)
from app.modules.matches.use_cases.get_match_by_id_use_case import GetMatchByIdUseCase
from app.modules.matches.use_cases.get_matches_use_case import GetMatchesUseCase
from app.modules.matches.use_cases.get_my_matches_use_case import GetMyMatchesUseCase
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
    response_model=MatchListResponseSchema,
)
async def get_matches(
    sport: SportType | None = None,
    skill_level: SkillLevel | None = None,
    status: MatchStatus | None = None,
    current_players: int | None = None,
    startdate: date | None = None,
    enddate: date | None = None,
    start_hour: int | None = None,
    end_hour: int | None = None,
    location: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(get_current_user),
):

    repository = SQLAlchemyMatchRepository(db)

    use_case = GetMatchesUseCase(repository)

    result = await use_case.execute(
        sport=sport,
        skill_level=skill_level,
        status=status,
        current_players=current_players,
        startdate=startdate,
        enddate=enddate,
        start_hour=start_hour,
        end_hour=end_hour,
        location=location,
        page=page,
        page_size=page_size,
    )

    matches = result["matches"]
    total = result["total"]

    return MatchListResponseSchema(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=ceil(total / page_size) if total else 0,
        matches=[MatchResponseSchema.model_validate(match) for match in matches],
    )


@router.get(
    "/me",
    response_model=MatchListResponseSchema,
)
async def get_my_matches(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):

    repository = SQLAlchemyMatchRepository(db)

    use_case = GetMyMatchesUseCase(repository)

    result = await use_case.execute(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )

    matches = result["matches"]
    total = result["total"]

    return MatchListResponseSchema(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=ceil(total / page_size) if total else 0,
        matches=[MatchResponseSchema.model_validate(match) for match in matches],
    )


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
