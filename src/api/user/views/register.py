from fastapi import Depends

from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from db.db_service import get_session

from src.api.user.router import router
from src.schemas.error import ErrorException
from src.schemas.user import User, UserCreate
from src.services.user import UserUtilitiesService


@router.post("/register", status_code=HTTP_200_OK, response_model=User,summary="Create new user", responses={
                400: {"model": ErrorException, "detail": "Attribute error",
                      "message": "Check your username or password"}
            })
async def register(user: UserCreate, session: Session = Depends(get_session)):
    user_service = UserUtilitiesService(session)
    user = await user_service.user_register(user)
    return user