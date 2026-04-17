import click

from llama_deploy.client import Client
from llama_deploy.types.apiserver import StatusEnum

from .internal.config import ConfigProfile


@click.command()
@click.pass_obj  # config_profile
def status(config_profile: ConfigProfile) -> None:
    """Print the API Server status."""
    pass
