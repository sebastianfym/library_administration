from sqlalchemy.ext.asyncio import AsyncSession

from config import logger_config
from db.repositories.author import AuthorRepository
from src.schemas.author import AuthorCreate, Author


class AuthorUtilitiesService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_author(self, author: AuthorCreate) -> Author:
        """
        Функция для создания модели автора
        :param author:
        :return Author:
        """
        author_repository = AuthorRepository(self.session)
        author = await author_repository.create_author(author)
        logger_config.logger.info(f"Create author with last name: {author.first_name} and first name:{author.second_name}")
        return Author.from_orm(author)