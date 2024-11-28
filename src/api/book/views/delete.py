from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from config import oauth2_scheme
from db.db_service import get_session
from src.api.book.router import router
from src.schemas.error import ErrorException
from src.services.book import BookUtilitiesService


@router.delete("/{book_id}", status_code=HTTP_200_OK, summary="Delete book", responses={
                404: {"model": ErrorException, "detail": "Book not found",
                      "message": "The model is that id was not found"}
            })
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session),
                      token: str = Depends(oauth2_scheme)):
    book_service = BookUtilitiesService(session)
    await book_service.delete_book(book_id, token)
    return {"status_code": HTTP_200_OK, "detail": "book was delete"}