from fastapi import Depends, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_service import get_session
from src.api.book.router import router
from src.schemas.error import ErrorException
from src.services.book import BookUtilitiesService


@router.get("/", response_model=List, responses={
                400: {"model": ErrorException, "detail": "Attribute error",
                      "message": "An unavailable attribute"}
            })
async def get_books(
    title: Optional[str] = Query(None, description="Фильтр по названию книги"),
    author: Optional[str] = Query(None, description="Фильтр по имени автора"),
    year: Optional[int] = Query(None, description="Фильтр по году выпуска"),
    session: AsyncSession = Depends(get_session),
):
    book_service = BookUtilitiesService(session)
    books = await book_service.search_books(title=title, author=author, year=year)
    return books
