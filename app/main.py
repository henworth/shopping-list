from contextlib import asynccontextmanager

from fastapi import FastAPI
from mangum import Mangum

from app.config import settings
from app.database import Base, engine
from app.routers import health, shopping_list


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
app.include_router(health.router)

# AWS Lambda entry point. Mangum auto-detects the event source (API Gateway v1/v2,
# ALB, or Lambda Function URL) and adapts it to the FastAPI ASGI app.
handler = Mangum(app, lifespan="auto", api_gateway_base_path=settings.api_prefix)
