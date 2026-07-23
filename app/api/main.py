from contextlib import asynccontextmanager
from fastapi import FastAPI
import structlog

from app.core.logging import setup_logging
from app.observability.tracing import init_tracing

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
init_tracing(app)

# Register API routers
from app.api.routes.leads import router as leads_router
from app.api.routes.metrics import router as metrics_router

app.include_router(leads_router)
app.include_router(metrics_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
