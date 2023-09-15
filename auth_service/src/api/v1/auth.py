from http import HTTPStatus
from uuid import UUID

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Header, Query
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from api.v1.response_schemas import FastAPIErrorResponse, FastAPIResponse, FastAPISuccessResponse
from db.exceptions import UserAlreadyExists, UserNotFound
from models.entities import RoleName
from services.auth_service import AuthService, PasswordNotEqual, get_auth_service
from utils.jwt_checker import auth_required

router = APIRouter()

PASSWORD_REGEX = r"^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$"
# 1. (?=.*[0-9]) - строка содержит хотя бы одно число;
# 2. (?=.*[a-z]) - строка содержит хотя бы одну латинскую букву в нижнем регистре;
# 3. (?=.*[A-Z]) - строка содержит хотя бы одну латинскую букву в верхнем регистре;
# 4. 0-9a-zA-Z]{8,} - строка состоит не менее, чем из 8 вышеупомянутых символов.


@router.post(
    path="/sign_up/",
    responses={
        HTTPStatus.OK: {"model": FastAPISuccessResponse},
        HTTPStatus.CONFLICT: {"model": FastAPIErrorResponse},
    },
)
async def sign_up(
    email: EmailStr,
    password: str = Query(regex=PASSWORD_REGEX),
    auth_service: AuthService = Depends(get_auth_service),
) -> FastAPIResponse:
    """Зарегистрировать пользователя

    Args:
        email: электронная почта пользователя
        password: пароль пользователя.
    """
    try:
        await auth_service.sign_up(email=email, password=password)
        return JSONResponse(status_code=HTTPStatus.OK, content={"result": "OK"})
    except UserAlreadyExists as exc:
        return JSONResponse(status_code=HTTPStatus.CONFLICT, content={"detail": str(exc)})


@router.post(
    path="/sign_in/",
    responses={
        HTTPStatus.OK: {"model": FastAPISuccessResponse},
        HTTPStatus.CONFLICT: {"model": FastAPIErrorResponse},
        HTTPStatus.NOT_FOUND: {"model": FastAPIErrorResponse},
    },
)
async def sign_in(
    email: EmailStr,
    password: str = Query(min_length=8),
    auth_service: AuthService = Depends(get_auth_service),
    user_agent: str = Header(None, include_in_schema=False),
    authorize: AuthJWT = Depends(),
) -> FastAPIResponse:
    """Авторизовать пользователя

    Args:
        email: электронная почта пользователя
        password: пароль пользователя.
    """
    try:
        user = await auth_service.sign_in(email=email, password=password, auth_data={"device": user_agent})
        access_token, refresh_token = await auth_service.create_both_tokens(authorize, str(user.id))

        return JSONResponse(
            status_code=HTTPStatus.OK, content={"access_token": access_token, "refresh_token": refresh_token}
        )
    except PasswordNotEqual as exc:
        return JSONResponse(status_code=HTTPStatus.FORBIDDEN, content={"detail": str(exc)})
    except UserNotFound as exc:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": str(exc)})


@router.post(
    path="/change_password/",
    responses={
        HTTPStatus.OK: {"model": FastAPISuccessResponse},
        HTTPStatus.CONFLICT: {"model": FastAPIErrorResponse},
        HTTPStatus.NOT_FOUND: {"model": FastAPIErrorResponse},
    },
)
@auth_required([RoleName.ADMIN, RoleName.REGISTERED])
async def change_password(
    user_id: UUID,
    old: str = Query(min_length=8),
    new: str = Query(regex=PASSWORD_REGEX),
    auth_service: AuthService = Depends(get_auth_service),
    authorize: AuthJWT = Depends(),
) -> FastAPIResponse:
    """Сменить пароль пользователя

    Args:
        email: электронная почта пользователя
        old: страый пароль пользователя
        new: новый пароль пользователя
    """
    try:
        await auth_service.change_password(user_id=user_id, old_password=old, new_password=new)
        return JSONResponse(status_code=HTTPStatus.OK, content={"result": "OK"})
    except PasswordNotEqual as exc:
        return JSONResponse(status_code=HTTPStatus.FORBIDDEN, content={"detail": str(exc)})
    except UserNotFound as exc:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": str(exc)})


@router.post("/refresh/")
async def refresh(
    authorize: AuthJWT = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> JSONResponse:
    await authorize.jwt_refresh_token_required()
    current_user_id = await authorize.get_jwt_subject()
    await auth_service.revoke_both_tokens(authorize)
    new_access_token, refresh_token = await auth_service.create_both_tokens(authorize, current_user_id)

    return JSONResponse(status_code=HTTPStatus.OK, content={"refresh_token": new_access_token})


@router.delete("/logout/")
async def logout(authorize: AuthJWT = Depends(), auth_service: AuthService = Depends(get_auth_service)) -> JSONResponse:
    await authorize.jwt_refresh_token_required()
    await auth_service.revoke_both_tokens(authorize)

    return JSONResponse(status_code=HTTPStatus.OK, content={"result": "OK"})
