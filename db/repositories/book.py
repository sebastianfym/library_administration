from typing import Optional, List

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.book import Book, Author
from src.schemas.book import BookCreate, BookEdit


class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_book(self, book: BookCreate) -> Book:
        """
        Функция для создания модели  книги
        :param BookCreate:
        :return Book:
        """
        book = Book(
            year=book.year,
            title=book.title,
            status=book.status,
            author_id=book.author_id,
        )
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def get_book(self, book_id: int) -> Book:
        """
        Функция для получения модели книги
        :param book_id:
        :return Book:
        """
        stmt = select(Book).where(Book.id == book_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def edit_book(self, book_id: int, updated_data: BookEdit) -> Book:
        """
        Функция для изменения модели  книги по id
        :param book_id:
        :param BookEdit:
        :return Book:
        """
        book = await self.get_book(book_id)
        if not book:
            return None
        for key, value in updated_data.dict(exclude_unset=True).items():
            if value == None:
                value = getattr(book, key)
            setattr(book, key, value)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete_book(self, book_id: int) -> bool:
        """
        Функция для удаления модели книги
        :param book_id:
        :return BooL:
        """
        tariff = await self.get_book(book_id)
        if not tariff:
            return False
        await self.session.delete(tariff)
        await self.session.commit()
        return True

    async def search_book(
            self,
            title: Optional[str] = None,
            author: Optional[str] = None,
            year: Optional[int] = None,
    ) -> List[Book]:
        """
        Функция для поиска модели  книги
        :param title:
        :param author:
        :param year:
        :return Book:
        """
        stmt = select(Book)

        if title:
            stmt = stmt.where(Book.title == title)
        if author:
            stmt = stmt.join(Author).where(
                or_(
                    Author.first_name == author,
                    Author.second_name == author
                )
            )
        if year:
            stmt = stmt.where(Book.year == year)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_books(self):
        """
        Функция для поиска всех моделей  книг
        :return List[Book]:
        """
        stmt = select(Book)
        result = await self.session.execute(stmt)
        return result.scalars().all()
