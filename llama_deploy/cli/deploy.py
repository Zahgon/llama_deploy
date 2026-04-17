from pathlib import Path

import click

from llama_deploy.client import Client

from .internal.config import ConfigProfile


@click.command()
@click.pass_obj  # config_profile
@click.option("--reload", is_flag=True)
@click.option(
    "--base-path",
    required=False,
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path),  # type: ignore
)
@click.argument(
    "deployment_config_file",
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path),  # type: ignore
)
def deploy(
    config_profile: ConfigProfile,
    reload: bool,
    deployment_config_file: Path,
    base_path: Path | None,
) -> None:
    """Create or reload a deployment."""
    pass
