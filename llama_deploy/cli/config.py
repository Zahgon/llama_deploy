import click
from pydantic import AnyHttpUrl
from rich.console import Console
from rich.table import Table

from .internal.config import Config, load_config


def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    pass


@click.group()
@click.pass_context
def config(ctx: click.Context) -> None:
    """Manage configuration profiles and settings.

    Loads the configuration from the specified config file and provides
    commands for viewing and modifying profiles.
    """
    pass


@click.command()
@click.pass_obj
def get_profiles(
    config: Config,
) -> None:
    """List all available configuration profiles."""
    pass


@click.command()
@click.pass_obj  # config_profile
def current_profile(
    config: Config,
) -> None:
    """Display the name of the currently active profile."""
    pass


@click.command()
@click.pass_obj  # config_profile
@click.argument("profile")
def use_profile(
    config: Config,
    profile: str,
) -> None:
    """Switch to using a different profile.

    Args:
        profile: Name of the profile to switch to

    Raises:
        ClickException: If the specified profile doesn't exist
    """
    pass


@click.command()
@click.pass_obj  # config_profile
@click.argument("param")
@click.argument("value")
def set_profile_vars(config: Config, param: str, value: str) -> None:
    """Set a variable for the current profile.

    Args:
        param: The parameter name to set
        value: The value to set for the parameter

    Raises:
        ClickException: If the parameter name is not valid
    """
    pass


@click.command()
@click.pass_obj
@click.argument("profile")
def delete_profile(
    config: Config,
    profile: str,
) -> None:
    """Delete a profile from the configuration.

    Args:
        profile: Name of the profile to delete

    Raises:
        ClickException: If the profile doesn't exist or is currently in use
    """
    pass


@click.command()
@click.pass_obj
@click.argument("old_name")
@click.argument("new_name")
def rename_profile(
    config: Config,
    old_name: str,
    new_name: str,
) -> None:
    """Rename a profile in the configuration.

    Args:
        old_name: Current name of the profile
        new_name: New name for the profile

    Raises:
        ClickException: If the old profile doesn't exist or the new name is already taken
    """
    pass


config.add_command(get_profiles)
config.add_command(current_profile)
config.add_command(use_profile)
config.add_command(set_profile_vars)
config.add_command(delete_profile)
config.add_command(rename_profile)
