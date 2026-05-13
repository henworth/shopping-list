from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine
from app.routers import shopping_list


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Shopping List API",
    version="0.1.0",
    root_path=settings.api_prefix,
    lifespan=lifespan,
)
app.include_router(shopping_list.router)
