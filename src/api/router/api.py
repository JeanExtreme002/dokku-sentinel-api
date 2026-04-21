import asyncio
import base64
import os
import tempfile
import shlex

from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import JSONResponse


def get_router(app: FastAPI) -> APIRouter:
    router = APIRouter()

    @router.post("/acl", response_description="Run dokku-acl command")
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
        
    @router.post("/ssh-keys/register", response_description="Register a SSH key")
    async def register_ssh_keys(request: Request, user: str, public_ssh_key: str):
        with tempfile.NamedTemporaryFile(
            mode="w+b", delete=False, suffix=".pub"
        ) as temp_file:
            content = base64.b64decode(public_ssh_key)
            temp_file.write(bytes(content))
            temp_file_path = temp_file.name

        command = f"dokku ssh-keys:add {user} {temp_file_path}"

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
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    return router
