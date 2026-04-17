import asyncio
import json
import logging
from typing import Annotated, AsyncGenerator, List, Optional

import httpx
import websockets
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
    WebSocket,
)
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.background import BackgroundTask
from workflows import Context
from workflows.context import JsonSerializer
from workflows.handler import WorkflowHandler

from llama_deploy.apiserver.deployment import Deployment
from llama_deploy.apiserver.deployment_config_parser import DeploymentConfig
from llama_deploy.apiserver.server import manager
from llama_deploy.types import (
    DeploymentDefinition,
    EventDefinition,
    SessionDefinition,
    TaskDefinition,
)
from llama_deploy.types.core import TaskResult, generate_id

deployments_router = APIRouter(
    prefix="/deployments",
)
logger = logging.getLogger(__name__)


def deployment(deployment_name: str) -> Deployment:
    """FastAPI dependency to retrieve a Deployment instance"""
    pass


@deployments_router.get("/")
async def read_deployments() -> list[DeploymentDefinition]:
    """Returns a list of active deployments."""
    pass


@deployments_router.get("/{deployment_name}")
async def read_deployment(
    deployment: Annotated[Deployment, Depends(deployment)],
) -> DeploymentDefinition:
    """Returns the details of a specific deployment."""
    pass


@deployments_router.post("/create")
async def create_deployment(
    base_path: str = ".",
    config_file: UploadFile = File(...),
    reload: bool = False,
    local: bool = False,
) -> DeploymentDefinition:
    """Creates a new deployment by uploading a configuration file."""
    pass


@deployments_router.post("/{deployment_name}/tasks/run")
async def create_deployment_task(
    deployment: Annotated[Deployment, Depends(deployment)],
    task_definition: TaskDefinition,
    session_id: str | None = None,
) -> JSONResponse:
    """Create a task for the deployment, wait for result and delete associated session."""
    pass


@deployments_router.post("/{deployment_name}/tasks/create")
async def create_deployment_task_nowait(
    deployment: Annotated[Deployment, Depends(deployment)],
    task_definition: TaskDefinition,
    session_id: str | None = None,
) -> TaskDefinition:
    """Create a task for the deployment but don't wait for result."""
    pass


@deployments_router.post("/{deployment_name}/tasks/{task_id}/events")
async def send_event(
    deployment: Annotated[Deployment, Depends(deployment)],
    task_id: str,
    session_id: str,
    event_def: EventDefinition,
) -> EventDefinition:
    """Send a human response event to a service for a specific task and session."""
    pass


@deployments_router.get("/{deployment_name}/tasks/{task_id}/events")
async def get_events(
    deployment: Annotated[Deployment, Depends(deployment)],
    session_id: str,
    task_id: str,
    raw_event: bool = False,
) -> StreamingResponse:
    """
    Get the stream of events from a given task and session.

    Args:
        raw_event (bool, default=False): Whether to return the raw event object
            or just the event data.
    """
    pass


@deployments_router.get("/{deployment_name}/tasks/{task_id}/results")
async def get_task_result(
    deployment: Annotated[Deployment, Depends(deployment)],
    session_id: str,
    task_id: str,
) -> TaskResult | None:
    """Get the task result associated with a task and session."""
    pass


@deployments_router.get("/{deployment_name}/tasks")
async def get_tasks(
    deployment: Annotated[Deployment, Depends(deployment)],
) -> list[TaskDefinition]:
    """Get all the tasks from all the sessions in a given deployment."""
    pass


@deployments_router.get("/{deployment_name}/sessions")
async def get_sessions(
    deployment: Annotated[Deployment, Depends(deployment)],
) -> list[SessionDefinition]:
    """Get the active sessions in a deployment and service."""
    pass


@deployments_router.get("/{deployment_name}/sessions/{session_id}")
async def get_session(
    deployment: Annotated[Deployment, Depends(deployment)], session_id: str
) -> SessionDefinition:
    """Get the definition of a session by ID."""
    pass


@deployments_router.post("/{deployment_name}/sessions/create")
async def create_session(
    deployment: Annotated[Deployment, Depends(deployment)],
) -> SessionDefinition:
    """Create a new session for a deployment."""
    pass


@deployments_router.post("/{deployment_name}/sessions/delete")
async def delete_session(
    deployment: Annotated[Deployment, Depends(deployment)], session_id: str
) -> None:
    """Get the active sessions in a deployment and service."""
    pass


async def _ws_proxy(ws: WebSocket, upstream_url: str) -> None:
    """Proxy WebSocket connection to upstream server."""
    pass


@deployments_router.websocket("/{deployment_name}/ui/{path:path}")
@deployments_router.websocket("/{deployment_name}/ui")
async def websocket_proxy(
    websocket: WebSocket,
    deployment: Annotated[Deployment, Depends(deployment)],
    path: str | None = None,
) -> None:
    pass


@deployments_router.api_route(
    "/{deployment_name}/ui/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
)
@deployments_router.api_route(
    "/{deployment_name}/ui",
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
)
async def proxy(
    request: Request,
    deployment: Annotated[Deployment, Depends(deployment)],
    path: str | None = None,
) -> StreamingResponse:
    pass
