from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import api_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n======================")
    print(f"Dokumentacja: http://127.0.0.1:8000/docs")
    print(f"Monitoring:   http://127.0.0.1:8000/monitor")
    print("======================\n")
    yield

app = FastAPI(
    title="Library API",
    lifespan=lifespan
)

# Rejestracja głównego routera (który zawiera już w sobie Authors, Books, WebSocket i Views)
app.include_router(api_router)