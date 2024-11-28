from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.book import Book, Author
from src.schemas.author import AuthorCreate


class AuthorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_author(self, author: AuthorCreate) -> Author:
        """
        Функция для создания модели автора
        :param author:
        :return Author:
        """
        author = Author(
            first_name=author.first_name,
            second_name=author.second_name,
        )
        self.session.add(author)
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def get_author(self, author_id: int) -> Author:
        """
        Функция для получения модели автора по id
        :param author_id:
        :return Author:
        """
        stmt = select(Author).where(Author.id == author_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()