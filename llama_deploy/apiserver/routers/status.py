import httpx
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse

from llama_deploy.apiserver.server import manager
from llama_deploy.apiserver.settings import settings
from llama_deploy.types.apiserver import Status, StatusEnum

status_router = APIRouter(
    prefix="/status",
)


@status_router.get("/")
async def status() -> Status:
    pass


@status_router.get("/metrics")
async def metrics() -> PlainTextResponse:
    """Proxies the Prometheus metrics endpoint through the API Server.

    This endpoint is mostly used in serverless environments where the LlamaDeploy
    container cannot expose more than one port (e.g. Knative, Google Cloud Run).
    If Prometheus is not enabled, this endpoint returns an empty HTTP-204 response.
    """
    pass
