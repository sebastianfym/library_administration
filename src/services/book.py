from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from config import logger_config
from db.models.book import Book
from db.repositories.author import AuthorRepository
from db.repositories.book import BookRepository

from src.enums.enum import LogType, LogAction, BookStatus
from src.schemas.author import Author
from src.schemas.book import BookCreate, BookEdit, BookBase, BookDetail
from src.services.logger import log_action


class BookUtilitiesService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_book(self, book: BookCreate, token:str) -> BookBase:
        """
        Функция для создания модели книг
        :param book:
        :param token:
        :return BookBase:
        """
        if book.year is None or book.title is None or book.author_id is None:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Required field is missing")
        book_repository = BookRepository(self.session)
        book = await book_repository.create_book(book=book)
        await log_action(token, LogAction.CREATE, self.session)
        return BookBase.from_orm(book)

    async def delete_book(self, book_id: int, token:str):
        """
        Функция для удаления модели книг
        :param book_id:
        :param token:
        """
        tariff_repository = BookRepository(self.session)
        if await tariff_repository.delete_book(book_id) is False:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Book not found")
        await log_action(token, LogAction.DELETE, self.session)

    async def detail_book(self, book_id: int, token:str) -> BookBase:
        """
        Функция для представления детальной модели книги
        :param book_id:
        :param token:
        :return BookBase:
        """
        book_repository = BookRepository(self.session)
        book = await book_repository.get_book(book_id)
        if book is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Book not found")
        return BookBase.from_orm(book)

    async def edit_book(self, book_id, tariff_data: BookEdit, token:str) -> Book:
        """
        Функция для изменения модели книг
        :param book:
        :param token:
        :return Book:
        """
        tariff_repository = BookRepository(self.session)
        if tariff_data.status is not None and tariff_data.status not in BookStatus:
            raise ValueError(f"Invalid status value: {tariff_data.status}")
        elif tariff_data.author_id is not None:
            author_repository = AuthorRepository(self.session)
            if await author_repository.get_author(tariff_data.author_id) is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Author not found")
        book = await tariff_repository.edit_book(book_id, tariff_data)
        if book is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Book not found")
        await log_action(token, LogAction.EDIT, self.session)
        return book


    async def formatting_books(self, book_list: List) -> List:
        """
        Функция для форматирования моделей книг
        :param book:
        :param token:
        :return List[BookBase]:
        """
        result_list = []
        for book in book_list:
            result_list.append(
                BookDetail(
                    id=book.id,
                    year=book.year,
                    title=book.title,
                    status=book.status,
                    author_id=book.author_id,
                    author=Author(
                        id=book.author.id,
                        first_name=book.author.first_name,
                        second_name=book.author.second_name
                    )
                )
            )
        return result_list

    async def search_books(self, title=None, author=None, year=None) -> List:
        """
        Функция для поиска моделей книг с аргументами для поиска
        :param title:
        :param author:
        :param year:
        :return List[BookBase]:
        """
        book_repository = BookRepository(self.session)
        if title is None and author is None and year is None:
            result = await book_repository.list_books()
        else:
            result = await book_repository.search_book(title, author, year)
            result = [BookBase.from_orm(book) for book in result]
        result_list = await self.formatting_books(result)
        return result_list
