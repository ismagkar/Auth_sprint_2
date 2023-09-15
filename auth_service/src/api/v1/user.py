from http import HTTPStatus
from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from api.v1.response_schemas import FastAPIErrorResponse, FastAPIResponse, FastAPISuccessResponse
from db.exceptions import UserNotFound
from models.entities import RoleName
from services.exceptions import BindEmptyRoles, BindUnknownRoles
from services.user_service import UserService, get_user_service
from utils.jwt_checker import auth_required

router = APIRouter()


@router.post(
    path="/bind/",
    responses={
        HTTPStatus.OK: {"model": FastAPISuccessResponse},
        HTTPStatus.BAD_REQUEST: {"model": FastAPIErrorResponse},
        HTTPStatus.NOT_FOUND: {"model": FastAPIErrorResponse},
    },
)
@auth_required([RoleName.ADMIN])
async def bind(
    user_id: UUID,
    role_ids: list[UUID] = Query(default=[]),
    user_service: UserService = Depends(get_user_service),
    authorize: AuthJWT = Depends(),
) -> FastAPIResponse:
    """Привязать пользователю роль

    Args:
        user_id: идентификатор пользователя
        role_ids: идентификаторы ролей
    """
    try:
        await user_service.bind(user_id=user_id, role_ids=role_ids)
        return JSONResponse(status_code=HTTPStatus.OK, content={"result": "OK"})
    except (BindEmptyRoles, BindUnknownRoles, UserNotFound) as exc:
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"detail": str(exc)})


@router.get(
    path="/history/",
    responses={
        HTTPStatus.OK: {"model": FastAPISuccessResponse},
        HTTPStatus.BAD_REQUEST: {"model": FastAPIErrorResponse},
    },
)
@auth_required([RoleName.ADMIN])
async def history(
    user_id: UUID,
    page_size: int = Query(default=50, gt=0),
    page_number: int = Query(default=1, gt=0),
    user_service: UserService = Depends(get_user_service),
    authorize: AuthJWT = Depends(),
) -> FastAPIResponse:
    """Привязать пользователю роль

    Args:
        user_id: идентификатор пользователя
        page_size: количество записей на странице
        page_number: номер страницы
    """
    offset = (page_number - 1) * page_size
    try:
        histories = await user_service.history(user_id=user_id, limit=page_size, offset=offset)
        return JSONResponse(status_code=HTTPStatus.OK, content={"result": [history.as_dict() for history in histories]})
    except UserNotFound as exc:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": str(exc)})


@router.get(
    path="/all/",
    responses={
        HTTPStatus.OK: {"model": FastAPISuccessResponse},
        HTTPStatus.BAD_REQUEST: {"model": FastAPIErrorResponse},
    },
)
@auth_required([RoleName.ADMIN])
async def users(
    page_size: int = Query(default=50, gt=0),
    page_number: int = Query(default=1, gt=0),
    user_service: UserService = Depends(get_user_service),
    authorize: AuthJWT = Depends(),
) -> FastAPIResponse:
    """Получить всех пользователей

    Args:
        page_size: количество записей на странице
        page_number: номер страницы
    """
    offset = (page_number - 1) * page_size
    try:
        users = await user_service.all(limit=page_size, offset=offset)
        return JSONResponse(status_code=HTTPStatus.OK, content={"result": [user.as_dict() for user in users]})
    except UserNotFound as exc:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": str(exc)})
