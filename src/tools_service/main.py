import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from tools_service.config import get_settings
from tools_service.db import init_db
from tools_service.log import setup_logging
from tools_service.routers import health, tools, webhooks

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(settings.log_level)
    await init_db(settings.database_path)
    logger.info("startup", extra={"fields": {"db": settings.database_path}})
    yield
    logger.info("shutdown")


def create_app() -> FastAPI:
    app = FastAPI(title="Agent Tools Service", version="0.1.0", lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(tools.router)
    app.include_router(webhooks.router)
    return app


app = create_app()
