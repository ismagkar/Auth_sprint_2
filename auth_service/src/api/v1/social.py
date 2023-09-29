import enum

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseConfig
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from core.oauth_config import oauth
from models.entities import SocialNetwork


router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/login/{social_network}')
async def login_by_social(request: Request, social_network: SocialNetwork):
    yandex = oauth.create_client('yandex')
    redirect_uri = request.url_for('auth_by_social_network', social_network='yandex')
    return await yandex.authorize_redirect(request, redirect_uri)


@router.get('/', response_class=HTMLResponse)
async def root_page(request: Request):

    yandex_oatuh_url = '#'
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            # 'google_authorization_url': google_authorization_url,
            'yandex_authorization_url': yandex_oatuh_url,
            # 'code': code,
        }
    )


@router.get('/callback/{social_network}')
async def auth_by_social_network(
        request: Request,
        social_network: SocialNetwork
):
    yandex = oauth.create_client('yandex')
    token = await yandex.authorize_access_token(request)
    resp = await yandex.get('info', token=token)
    resp.raise_for_status()
    profile = resp.json()
    return {
        'token': token,
        'user': profile,
    }