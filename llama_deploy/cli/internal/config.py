from pathlib import Path
from typing import cast

import yaml
from pydantic import BaseModel, Field
from typing_extensions import Self

from .utils import DEFAULT_PROFILE_NAME, _default_config_path


class ConfigProfile(BaseModel):
    """Pydantic model representing a llamactl configuration profile."""

    server: str = "http://localhost:4501"
    insecure: bool = False
    timeout: float = 120.0


class Config(BaseModel):
    """Pydantic model representing a llamactl configuration."""

    current_profile: str
    profiles: dict[str, ConfigProfile]
    path: Path = Field(default_factory=_default_config_path)

    @classmethod
    def from_path(cls, config_file_path: Path) -> Self:
        """Get a Config instance from a configuration file."""
        pass

    def write(self) -> None:
        """Write the Config object in the configuration file."""
        pass


def load_config(path: Path | None = None) -> Config:
    pass
