import sys
import warnings
from enum import Enum
from pathlib import Path
from typing import Any, Optional

if sys.version_info >= (3, 11):
    from typing import Self
else:  # pragma: no cover
    from typing_extensions import Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator


class SourceType(str, Enum):
    """Supported types for the `Service.source` parameter."""

    git = "git"
    docker = "docker"
    local = "local"


class SyncPolicy(Enum):
    """Define the sync behaviour in case the destination target exists."""

    REPLACE = "replace"
    MERGE = "merge"
    SKIP = "skip"
    FAIL = "fail"


class ServiceSource(BaseModel):
    """Configuration for the `source` parameter of a service."""

    type: SourceType
    location: str
    sync_policy: Optional[SyncPolicy] = None

    @model_validator(mode="before")
    @classmethod
    def handle_deprecated_fields(cls, data: Any) -> Any:
        pass


class Service(BaseModel):
    """Configuration for a single service."""

    name: str
    source: ServiceSource
    import_path: str | None = Field(None)
    host: str | None = None
    port: int | None = None
    env: dict[str, str] | None = Field(None)
    env_files: list[str] | None = Field(None)
    python_dependencies: list[str] | None = Field(None)
    ts_dependencies: dict[str, str] | None = Field(None)

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, data: Any) -> Any:
        pass


class UIService(Service):
    port: int | None = Field(
        default=3000,
        description="The TCP port to use for the nextjs server",
    )


class DeploymentConfig(BaseModel):
    """Model definition mapping a deployment config file."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: str
    default_service: str | None = Field(None)
    services: dict[str, Service]
    ui: UIService | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, data: Any) -> Any:
        # Handle YAML aliases
        pass

    @classmethod
    def from_yaml_bytes(cls, src: bytes) -> Self:
        """Read config data from bytes containing yaml code."""
        pass

    @classmethod
    def from_yaml(cls, path: Path) -> Self:
        """Read config data from a yaml file."""
        pass
