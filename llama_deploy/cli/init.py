import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Type

import click
import yaml
from pydantic import BaseModel

# Import pydantic models
from llama_deploy.apiserver.deployment_config_parser import (
    DeploymentConfig,
    Service,
    ServiceSource,
    SourceType,
    UIService,
)


@click.command()
@click.option(
    "--name",
    type=str,
    default=None,
    help="Name of the project to create",
)
@click.option(
    "--destination",
    type=str,
    default=None,
    help="Directory where the project will be created",
)
@click.option(
    "--template",
    type=click.Choice(["basic", "none"]),  # For future: add more templates
    default=None,
    help="Template to use for the workflow (currently only 'basic' is supported)",
)
def init(
    name: Optional[str] = None,
    destination: Optional[str] = None,
    template: Optional[str] = None,
) -> None:
    """Bootstrap a new llama-deploy project with a basic workflow and configuration."""
    pass


def write_yaml_with_comments(
    file_path: Path, config: Dict[str, Any], model: DeploymentConfig
) -> None:
    """Write YAML with comments based on pydantic model schemas and field descriptions."""
    pass


def create_deployment_config(name: str, use_ui: bool = False) -> DeploymentConfig:
    """Create a deployment configuration using pydantic models."""
    pass
