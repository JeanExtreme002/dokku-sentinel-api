from fastapi import APIRouter, Depends, FastAPI

from src.api.router.api import get_router as api_router
from src.api.tools.validator import validate_admin


def get_router(app: FastAPI) -> APIRouter:
    router = APIRouter()

    router.include_router(
        api_router(router),
        tags=["Api"],
        prefix="/api",
        dependencies=[
            Depends(validate_admin),
        ],
    )

    return router
