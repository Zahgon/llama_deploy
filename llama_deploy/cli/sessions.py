import click

from llama_deploy.client import Client

from .internal.config import ConfigProfile


@click.group()
def sessions() -> None:
    """Manage sessions for a given deployment."""
    pass


@click.command()
@click.pass_obj  # config_profile
@click.option(
    "-d", "--deployment", required=True, is_flag=False, help="Deployment name"
)
@click.pass_context
def create(
    ctx: click.Context,
    config_profile: ConfigProfile,
    deployment: str,
) -> None:
    pass


sessions.add_command(create)
