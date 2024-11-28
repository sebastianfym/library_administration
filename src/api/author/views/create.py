from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from config import oauth2_scheme
from db.db_service import get_session


from src.api.author.router import router
from src.schemas.author import Author, AuthorCreate
from src.schemas.error import ErrorException
from src.services.author import AuthorUtilitiesService


@router.post("/", status_code=HTTP_200_OK, summary="Create a new author", responses={
                400: {"model": ErrorException, "detail": "unexpected error",
                      "message": "Bad request"}
            })
async def create_author(data: AuthorCreate, session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    author_service = AuthorUtilitiesService(session)
    try:
        author = await author_service.create_author(data)
        return {"status_code": HTTP_200_OK, "detail": author}
    except Exception as error:
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error)
