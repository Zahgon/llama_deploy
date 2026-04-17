import os
import subprocess
from pathlib import Path
from typing import Optional

import click
from prometheus_client import start_http_server
from tenacity import RetryError, Retrying, stop_after_attempt, wait_fixed

from llama_deploy.apiserver.settings import settings
from llama_deploy.client import Client

RETRY_WAIT_SECONDS = 1


@click.command()
@click.argument(
    "deployment_file",
    required=False,
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path),  # type: ignore
)
def serve(deployment_file: Path | None) -> None:
    """Run the API Server in the foreground."""
    pass
