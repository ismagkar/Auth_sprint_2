import asyncio
import logging
from functools import wraps

import typer
from sqlalchemy import select

from db.postgres import async_database_session
from models.entities import Role, RoleName, User

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def typer_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@typer_async
async def create_admin(email: str = "admin@mail.ru", password: str = "Password123") -> None:
    async with async_database_session() as session:
        admin_role = (await session.execute(select(Role).where(Role.name == RoleName.ADMIN))).scalar()
        user = User(email=email, password=password, roles=[admin_role])
        session.add(user)
        try:
            await session.commit()
            logger.info(f"Администратор успешно добавлен: email={email}; пароль={password}")
        except Exception:
            logger.exception("Ошибка добавления администратора")


if __name__ == "__main__":
    typer.run(create_admin)
