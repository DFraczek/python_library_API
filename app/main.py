from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.api_v1 import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n========================================")
    print("Dokumentacja: http://127.0.0.1:8000/docs")
    print("========================================")
    yield


app = FastAPI(
    title="Library API",
    lifespan=lifespan
)

app.include_router(api_router)