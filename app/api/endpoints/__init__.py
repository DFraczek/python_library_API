from fastapi import APIRouter, Depends

from app.api.endpoints import authors, books, genres, websocket, reviews, views, auth
from app.core.dependencies import get_current_user

api_router = APIRouter()

api_router.include_router(
    authors.router,
    prefix="/authors",
    tags=["Authors"],
    dependencies=[Depends(get_current_user)],
)
api_router.include_router(
    books.router,
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(get_current_user)],
)
api_router.include_router(
    genres.router,
    prefix="/genres",
    tags=["Genres"],
    dependencies=[Depends(get_current_user)],
)
api_router.include_router(
    reviews.router,
    prefix="/reviews",
    tags=["Reviews"],
    dependencies=[Depends(get_current_user)],
)
api_router.include_router(websocket.router, tags=["Status"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(views.router)