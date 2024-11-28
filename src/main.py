import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.api.book.router import router as book_router
from src.api.user.router import router as user_router
from src.api.author.router import router as author_router

from config import settings

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

v1 = APIRouter(prefix="/api/v1")
v1.include_router(book_router)
v1.include_router(user_router)
v1.include_router(author_router)


app.include_router(v1)
