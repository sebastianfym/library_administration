from starlette.status import HTTP_200_OK
from src.api.user.router import router

from fastapi import Depends, status
from sqlalchemy.orm import Session


from db.db_service import get_session
from src.schemas.error import ErrorException
from src.schemas.user import TokenRefreshRequestSchema, UserAuthSchema
from src.services.user import UserUtilitiesService


@router.post("/login", status_code=HTTP_200_OK, summary="User authorization page", responses={
                401: {"model": ErrorException, "detail": "Unauthorized",
                      "message": "Incorrect username or password"}
            })
async def login(user_data: UserAuthSchema, session: Session = Depends(get_session)):
    user_service = UserUtilitiesService(session)
    access_token, refresh_token = await user_service.user_auth(user_data)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", status_code=status.HTTP_200_OK, summary="Refresh access token", responses={
                401: {"model": ErrorException, "detail": "Invalid refresh token",
                      "message": "Invalid refresh token"}
            })
async def refresh_token(request: TokenRefreshRequestSchema, session: Session = Depends(get_session)):
    user_service = UserUtilitiesService(session)
    access_token, refresh_token = await user_service.refresh_token(refresh_token = request.refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token}