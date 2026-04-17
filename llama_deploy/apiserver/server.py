import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from .deployment import Manager
from .deployment_config_parser import DeploymentConfig
from .settings import settings
from .stats import apiserver_state

logger = logging.getLogger("uvicorn.info")
manager = Manager()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    pass
