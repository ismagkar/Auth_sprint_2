from http import HTTPStatus
from pprint import pprint

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Header
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from core.oauth_config import oauth
from db.exceptions import UserNotFound
from models.entities import SocialNetwork
from services.auth_service import AuthService, get_auth_service

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/login/{social_network}')
async def login_by_social(request: Request, social_network: SocialNetwork):
    client = oauth.create_client(social_network.value)
    redirect_uri = request.url_for(
        'auth_by_social_network', social_network=social_network.value
    )
    return await client.authorize_redirect(request, redirect_uri)


@router.get('/', response_class=HTMLResponse)
async def root_page(request: Request):

    yandex_oatuh_url = request.url_for(
        'login_by_social', social_network=SocialNetwork.yandex.value
    )
    google_oatuh_url = request.url_for(
        'login_by_social', social_network=SocialNetwork.google.value)

    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'google_authorization_url': google_oatuh_url,
            'yandex_authorization_url': yandex_oatuh_url,
        }
    )


@router.get('/callback/{social_network}')
async def auth_by_social_network(
        request: Request,
        social_network: SocialNetwork,
        auth_service: AuthService = Depends(get_auth_service),
        user_agent: str = Header(None, include_in_schema=False),
        authorize: AuthJWT = Depends(),
):
    client = oauth.create_client(social_network.value)
    token = await client.authorize_access_token(request)
    resp = await client.get('info', token=token)

    resp.raise_for_status()
    profile = resp.json()

    auth_profile = {
        'email': profile.get('default_email'),
        'social_id': profile.get('id'),
        'social_name': social_network.name
    }

    try:
        user = await auth_service.auth_by_social(auth_profile=auth_profile, auth_data={"device": user_agent})
        access_token, refresh_token = await auth_service.create_both_tokens(authorize, str(user.id))

        return JSONResponse(
            status_code=HTTPStatus.OK, content={"access_token": access_token, "refresh_token": refresh_token}
        )
    except UserNotFound as exc:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": str(exc)})
