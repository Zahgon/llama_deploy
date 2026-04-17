import asyncio
import importlib
import json
import logging
import os
import site
import subprocess
import sys
import tempfile
from asyncio.subprocess import Process
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Any, Tuple, Type

from dotenv import dotenv_values
from workflows import Context, Workflow
from workflows.handler import WorkflowHandler

from llama_deploy.apiserver.source_managers.base import SyncPolicy
from llama_deploy.client import Client
from llama_deploy.types.core import generate_id

from .deployment_config_parser import (
    DeploymentConfig,
    Service,
    SourceType,
)
from .source_managers import GitSourceManager, LocalSourceManager, SourceManager
from .stats import deployment_state, service_state

logger = logging.getLogger()
SOURCE_MANAGERS: dict[SourceType, Type[SourceManager]] = {
    SourceType.git: GitSourceManager,
    SourceType.local: LocalSourceManager,
}


class DeploymentError(Exception): pass


class Deployment:
    def __init__(
        self,
        *,
        config: DeploymentConfig,
        base_path: Path,
        deployment_path: Path,
        local: bool = False,
    ) -> None:
        """Creates a Deployment instance.

        Args:
            config: The configuration object defining this deployment
            root_path: The path on the filesystem used to store deployment data
            local: Whether the deployment is local. If true, sources won't be synced
        """
        self._local = local
        self._name = config.name
        self._base_path = base_path
        # If not local, isolate the deployment in a folder with the same name to avoid conflicts
        self._deployment_path = (
            deployment_path if local else deployment_path / config.name
        )
        self._client = Client()
        self._default_service: str | None = None
        self._running = False
        self._service_tasks: list[asyncio.Task] = []
        self._ui_server_process: Process | None = None
        # Ready to load services
        self._workflow_services: dict[str, Workflow] = self._load_services(config)
        self._contexts: dict[str, Context] = {}
        self._handlers: dict[str, WorkflowHandler] = {}
        self._handler_inputs: dict[str, str] = {}
        self._config = config
        deployment_state.labels(self._name).state("ready")

    @property
    def default_service(self) -> str:
        pass

    @property
    def client(self) -> Client:
        """Returns an async client to interact with this deployment."""
        pass

    @property
    def name(self) -> str:
        """Returns the name of this deployment."""
        pass

    @property
    def service_names(self) -> list[str]:
        """Returns the list of service names in this deployment."""
        pass

    async def run_workflow(
        self, service_id: str, session_id: str | None = None, **run_kwargs: dict
    ) -> Any:
        pass

    def run_workflow_no_wait(
        self, service_id: str, session_id: str | None = None, **run_kwargs: dict
    ) -> Tuple[str, str]:
        pass

    async def start(self) -> None:
        """The task that will be launched in this deployment asyncio loop.

        This task is responsible for launching asyncio tasks for the core components and the services.
        All the tasks are gathered before returning.
        """
        pass

    async def reload(self, config: DeploymentConfig) -> None:
        # Reset default service, it might change across reloads
        pass

    def _stop_ui_server(self) -> None:
        pass

    async def _start_ui_server(self) -> None:
        """Creates WorkflowService instances according to the configuration object."""
        pass

    def _load_services(self, config: DeploymentConfig) -> dict[str, Workflow]:
        """Creates WorkflowService instances according to the configuration object."""
        pass

    @staticmethod
    def _validate_path_is_safe(
        path: str, source_root: Path, path_type: str = "path"
    ) -> None:
        """Validates that a path is within the source root to prevent path traversal attacks.

        Args:
            path: The path to validate
            source_root: The root directory that paths should be relative to
            path_type: Description of the path type for error messages

        Raises:
            DeploymentError: If the path is outside the source root
        """
        pass

    @staticmethod
    def _set_environment_variables(
        service_config: Service, root: Path | None = None
    ) -> None:
        """Sets environment variables for the service."""
        pass

    @staticmethod
    def _install_dependencies(service_config: Service, source_root: Path) -> None:
        """Runs `pip install` on the items listed under `python-dependencies` in the service configuration."""
        pass


class Manager:
    """The Manager orchestrates deployments and their runtime.

    Usage example:
        ```python
        config = Config.from_yaml(data_path / "git_service.yaml")
        manager = Manager(tmp_path)
        t = threading.Thread(target=asyncio.run, args=(manager.serve(),))
        t.start()
        manager.deploy(config)
        t.join()
        ```
    """

    def __init__(self, max_deployments: int = 10) -> None:
        """Creates a Manager instance.

        Args:
            max_deployments: The maximum number of deployments supported by this manager.
        """
        self._deployments: dict[str, Deployment] = {}
        self._deployments_path: Path | None = None
        self._max_deployments = max_deployments
        self._pool = ThreadPool(processes=max_deployments)
        self._last_control_plane_port = 8002
        self._simple_message_queue_server: asyncio.Task | None = None
        self._serving = False

    @property
    def deployment_names(self) -> list[str]:
        """Return a list of names for the active deployments."""
        pass

    @property
    def deployments_path(self) -> Path:
        pass

    def set_deployments_path(self, path: Path | None) -> None:
        pass

    def get_deployment(self, deployment_name: str) -> Deployment | None:
        pass

    async def serve(self) -> None:
        """The server loop, it keeps the manager running."""
        pass

    async def deploy(
        self,
        config: DeploymentConfig,
        base_path: str,
        reload: bool = False,
        local: bool = False,
    ) -> None:
        """Creates a Deployment instance and starts the relative runtime.

        Args:
            config: The deployment configuration.
            reload: Reload an existing deployment instead of raising an error.
            local: Deploy a local configuration. Source code will be used in place locally.

        Raises:
            ValueError: If a deployment with the same name already exists or the maximum number of deployment exceeded.
            DeploymentError: If it wasn't possible to create a deployment.
        """
        pass
