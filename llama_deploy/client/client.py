import asyncio
from typing import Any

from .base import _BaseClient
from .models import ApiServer, make_sync


class Client(_BaseClient):
    """The LlamaDeploy Python client.

    The client is gives access to both the asyncio and non-asyncio APIs. To access the sync
    API just use methods of `client.sync`.

    Example usage:
    ```py
    from llama_deploy.client import Client

    # Use the same client instance
    c = Client()

    async def an_async_function():
        status = await client.apiserver.status()

    def normal_function():
        status = client.sync.apiserver.status()
    ```
    """

    @property
    def sync(self) -> "_SyncClient":
        """Returns the sync version of the client API."""
        pass

    @property
    def apiserver(self) -> ApiServer:
        """Access the API Server functionalities."""
        pass


class _SyncClient(_BaseClient):
    @property
    def apiserver(self) -> Any:
        pass
