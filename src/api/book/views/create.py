from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from config import oauth2_scheme
from db.db_service import get_session

from src.api.book.router import router
from src.schemas.book import BookCreate
from src.schemas.error import ErrorException
from src.services.book import BookUtilitiesService


@router.post("/", status_code=HTTP_200_OK, summary="Create a new book", responses={
                400: {"model": ErrorException, "detail": "field is missing",
                      "message": "Required field is missing"}
            })
async def create_book(book_data: BookCreate, session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    book_service = BookUtilitiesService(session)
    try:
        book = await book_service.create_book(book_data, token)
        return {"status_code": HTTP_200_OK, "detail":book}
    except Exception as error:
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error)
