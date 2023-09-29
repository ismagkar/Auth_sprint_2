import uvicorn
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse, ORJSONResponse
from redis.asyncio import Redis
from fastapi.staticfiles import StaticFiles

from api.v1 import auth, role, user, social
from core.config import settings
from core.jwt_config import setting_jwt
from db import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.redis_db.host, port=settings.redis_db.port)
    yield
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.mount('/static', StaticFiles(directory='static'), name='static')

@AuthJWT.load_config
def get_config():
    return setting_jwt


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    entry = await redis.redis.get(jti)
    return entry


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/healthcheck")
async def health_check() -> str:
    return "OK"


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/user", tags=["user"])
app.include_router(role.router, prefix="/api/v1/role", tags=["role"])
app.include_router(social.router, prefix="/api/v1/social", tags=["social"])



if __name__ == "__main__":
    uvicorn.run(app="main:app", host=settings.host, port=settings.port, reload=True)
