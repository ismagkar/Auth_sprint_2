from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory='templates')

oauth = OAuth()
oauth.register(
    'yandex',
    client_id='',
    client_secret=''
)


@router.get('/', response_class=HTMLResponse)
def logon(request: Request):
    yandex_authorization_url = '#'
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            # 'google_authorization_url': google_authorization_url,
            'yandex_authorization_url': yandex_authorization_url,
            # 'code': code,
        }
    )


@router.post('/login/{social_name}')
def signin_by_social_network(
        request: Request,
):
    return True