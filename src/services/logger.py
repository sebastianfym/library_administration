from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from config import logger_config
from db.repositories.user import UserRepository
from src.enums.enum import LogAction
from src.services.auth import AuthUtilitiesService


async def log_action(token: str, action: LogAction, session: AsyncSession):
    """
    Функция для создания текста логирования
    :param action:
    :param token:
    :param session:
    :return None:
    """
    payload = AuthUtilitiesService.verify_token(token)
    user_repository = UserRepository(session)
    user = await user_repository.get_current_user(payload)
    logg = f"User: unauthorized;\nAction: {action.value} book;\nTime:{datetime.now()}"
    if user is not None:
        logg = f"User: {user.id};\nAction: {action.value} book;\nTime:{datetime.now()}"

    logger_config.logger.info(logg)
