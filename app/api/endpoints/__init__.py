from fastapi import APIRouter
from app.api.endpoints import authors, books, genres, websocket, reviews, views

api_router = APIRouter()

api_router.include_router(authors.router, prefix="/authors", tags=["Authors"])
api_router.include_router(books.router, prefix="/books", tags=["Books"])
api_router.include_router(genres.router, prefix="/genres", tags=["Genres"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(websocket.router, tags=["Status"])
api_router.include_router(views.router)