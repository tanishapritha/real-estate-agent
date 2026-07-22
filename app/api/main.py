from contextlib import asynccontextmanager
from fastapi import FastAPI
import structlog

from app.core.logging import setup_logging

setup_logging()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting_up_api")
    yield
    logger.info("shutting_down_api")


app = FastAPI(
    title="RealEstate AI Sales OS",
    description="Stateful multi-agent workflow platform for real-estate sales",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
