"""Client functionalities to operate on the API Server.

This module allows the client to use all the functionalities
from the LlamaDeploy API Server. For this to work, the API
Server must be up and its URL (by default `http://localhost:4501`)
reachable by the host executing the client code.
"""

import asyncio
import json
from typing import Any, AsyncGenerator, TextIO

import httpx
from pydantic import Field
from workflows.context import JsonSerializer
from workflows.events import Event

from llama_deploy.types.apiserver import Status, StatusEnum
from llama_deploy.types.core import (
    EventDefinition,
    SessionDefinition,
    TaskDefinition,
    TaskResult,
)

from .model import Collection, Model


class SessionCollection(Collection):
    """A model representing a collection of session for a given deployment."""

    deployment_id: str = Field(
        description="The ID of the deployment containing the sessions."
    )

    async def delete(self, session_id: str) -> None:
        """Deletes the session with the provided `session_id`.

        Args:
            session_id: The id of the session that will be removed

        Raises:
            HTTPException: If the session couldn't be found with the id provided.
        """
        pass

    async def create(self) -> SessionDefinition:
        """Create a new session."""
        pass

    async def list(self) -> list[SessionDefinition]:
        """Returns a collection of all the sessions in the given deployment."""
        pass

    async def get(self, id: str) -> SessionDefinition:
        """Gets a deployment by id."""
        get_url = f"{self.client.api_server_url}/deployments/{self.deployment_id}/sessions/{id}"
        await self.client.request(
            "GET",
            get_url,
            verify=not self.client.disable_ssl,
            timeout=self.client.timeout,
        )
        model_class = self._prepare(SessionDefinition)
        return model_class(client=self.client, id=id)


class Task(Model):
    """A model representing a task belonging to a given session in the given deployment."""

    deployment_id: str = Field(
        description="The ID of the deployment this task belongs to."
    )
    session_id: str = Field(description="The ID of the session this task belongs to.")

    async def results(self) -> TaskResult | None:
        """Returns the result of a given task."""
        pass

    async def send_event(self, ev: Event, service_name: str) -> EventDefinition:
        """Sends a human response event."""
        pass

    async def events(self) -> AsyncGenerator[dict[str, Any], None]:  # pragma: no cover
        """Returns a generator object to consume the events streamed from a service."""
        pass


class TaskCollection(Collection):
    """A model representing a collection of tasks for a given deployment."""

    deployment_id: str = Field(
        description="The ID of the deployment these tasks belong to."
    )

    async def run(self, task: TaskDefinition) -> Any:
        """Runs a task and returns the results once it's done.

        Args:
            task: The definition of the task we want to run.
        """
        run_url = (
            f"{self.client.api_server_url}/deployments/{self.deployment_id}/tasks/run"
        )
        if task.session_id:
            run_url += f"?session_id={task.session_id}"

        r = await self.client.request(
            "POST",
            run_url,
            verify=not self.client.disable_ssl,
            json=task.model_dump(),
            timeout=self.client.timeout,
        )

        return r.json()

    async def create(self, task: TaskDefinition) -> Task:
        """Runs a task returns it immediately, without waiting for the results."""
        pass

    async def list(self) -> list[Task]:
        """Returns the list of tasks from this collection."""
        pass


class Deployment(Model):
    """A model representing a deployment."""

    @property
    def tasks(self) -> TaskCollection:
        """Returns a collection of tasks from all the sessions in the given deployment."""
        pass

    @property
    def sessions(self) -> SessionCollection:
        """Returns a collection of all the sessions in the given deployment."""
        pass


class DeploymentCollection(Collection):
    """A model representing a collection of deployments currently active."""

    async def create(
        self, config: TextIO, base_path: str, reload: bool = False, local: bool = False
    ) -> Deployment:
        """Creates a new deployment from a deployment file.

        If `reload` is true, an existing deployment will be reloaded, otherwise
        an error will be raised.

        If `local` is true, the sync managers won't attempt at syncing data.
        This is mostly for supporting local development.

        Example:
            ```
            with open("deployment.yml") as f:
                await client.apiserver.deployments.create(f)
            ```
        """
        pass

    async def get(self, id: str) -> Deployment:
        """Gets a deployment by id."""
        get_url = f"{self.client.api_server_url}/deployments/{id}"
        # Current version of apiserver doesn't returns anything useful in this endpoint, let's just ignore it
        await self.client.request(
            "GET",
            get_url,
            verify=not self.client.disable_ssl,
            timeout=self.client.timeout,
        )
        model_class = self._prepare(Deployment)
        return model_class(client=self.client, id=id)

    async def list(self) -> list[Deployment]:
        """Return a list of Deployment instances for this collection."""
        pass


class ApiServer(Model):
    """A model representing the API Server instance."""

    async def status(self) -> Status:
        """Returns the status of the API Server."""
        pass

    @property
    def deployments(self) -> DeploymentCollection:
        """Returns a collection of deployments currently active in the API Server."""
        pass
