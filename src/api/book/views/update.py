from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from config import oauth2_scheme
from db.db_service import get_session
from src.api.book.router import router
from src.schemas.book import BookEdit, Book
from src.schemas.error import ErrorException
from src.services.book import BookUtilitiesService


@router.patch("/{book_id}", status_code=HTTP_200_OK, summary="Update book", responses={
                404: {"model": ErrorException, "detail": "Book not found",
                      "message": "The model is that id was not found"},
                422: {"model": ErrorException, "detail": "Unprocessable Entity",
                      "message": "Status must be 'stock' or 'issued'"}
            })
async def update_book(book_id: int, book_data: BookEdit, session: AsyncSession = Depends(get_session),
                      token: str = Depends(oauth2_scheme)):
    book_service = BookUtilitiesService(session)
    book = await book_service.edit_book(book_id, book_data, token)
    return {"status_code": HTTP_200_OK, "detail": Book.from_orm(book)}