import logging
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.router import get_router
from src.config import Config

APP_ROOT = Path(__file__).parent

scheduler = AsyncIOScheduler()


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of the application.
    """
    logging.basicConfig(level=Config.API_LOG_LEVEL.upper())

    _app = FastAPI(
        title="Dokku-Sentinel API",
        default_response_class=JSONResponse,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(get_router(_app))

    return _app
