from typing import Optional

from fastapi import HTTPException, Request, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from src.config import Config

MASTER_KEY = Config.MASTER_KEY

if MASTER_KEY is None:
    raise ValueError("MASTER_KEY must be set in the environment variables")


def validate_admin(
    request: Request,
    master_key_header: Optional[str] = Security(
        APIKeyHeader(
            name="MASTER-KEY",
            auto_error=False,
        )
    ),
) -> None:
    """
    Check if user is admin or master key is valid.
    """
    if master_key_header != MASTER_KEY:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or missing MASTER key"
        )
