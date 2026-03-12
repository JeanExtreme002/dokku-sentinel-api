import asyncio
import shlex

from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import JSONResponse


def get_router(app: FastAPI) -> APIRouter:
    router = APIRouter()

    @router.post("/run", response_description="Run dokku-acl command")
    async def run_command(request: Request, command: str):
        command = "dokku acl:" + command.strip()

        try:
            args = shlex.split(command)
            proc = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "command": command,
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode(),
                    "returncode": proc.returncode,
                    "status": proc.returncode == 0,
                },
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "command": command,
                    "stdout": "",
                    "stderr": str(e),
                    "returncode": -1,
                    "status": False,
                },
            )

    return router
