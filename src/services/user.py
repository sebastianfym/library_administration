from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from config import settings
from db.repositories.user import UserRepository
from src.schemas.user import User, UserCreate, UserAuthSchema
from src.services.auth import AuthUtilitiesService


class UserUtilitiesService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_user(self, username: str) -> None | User:
        """
        Функция для проверки пользователя по юзернейму
        :param username:
        :return User:
        """
        user_repository = UserRepository(self.session)
        return await user_repository.get_user_by_name(username)

    async def user_register(self, user_data: UserCreate) -> User:
        """
        Функция для регистрации пользователя
        :param user_data:
        :return User:
        """
        user_repository = UserRepository(self.session)
        if await self.check_user(user_data.username) is not None:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User already register")
        user = await user_repository.user_register(user_data)
        return user

    async def get_user_by_refresh_token(self, refresh_token: str) -> User:
        """
        Функция для регистрации пользователя
        :param user_data:
        :return User:
        """
        user_repository = UserRepository(self.session)
        try:
            user = await user_repository.get_user_by_refresh_token(refresh_token)
            return user
        except AttributeError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    async def user_auth(self, user_data: UserAuthSchema):
        """
        Функция авторизации пользователя
        :param user_data:
        :return User:
        """
        user_repository = UserRepository(self.session)
        user = await user_repository.auth_user(user_data.username)

        if (not user) or (not AuthUtilitiesService.verify_password(user_data.password, user.password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

        access_token, refresh_token = AuthUtilitiesService.create_tokens(
            user_id=user.id,
            access_expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        await user_repository.user_refresh_token(user.id)
        return access_token, refresh_token

    async def refresh_token(self, refresh_token: str):
        """
        Функция для восстановления пользователя по рефреш токену
        :param user_data:
        :return User:
        """
        user_repository = UserRepository(self.session)

        approve_refresh_token = await user_repository.check_and_get_refresh_token(refresh_token)
        user = await self.get_user_by_refresh_token(approve_refresh_token)

        access_token, refresh_token = AuthUtilitiesService.create_tokens(
            user_id=user.id,
            access_expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        await user_repository.user_refresh_token(str(user.id), refresh_token)
        return access_token, refresh_token