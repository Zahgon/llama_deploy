import shutil
from pathlib import Path
from typing import Any

from git import Repo

from .base import SourceManager, SyncPolicy


class GitSourceManager(SourceManager):
    """A SourceManager specialized for sources of type `git`."""

    def sync(
        self,
        source: str,
        destination: str | None = None,
        sync_policy: SyncPolicy = SyncPolicy.REPLACE,
    ) -> None:
        """Clones the repository at URL `source` into a local path `destination`.

        Args:
            source: The URL of the git repository. It can optionally contain a branch target using the name convention
                `git_repo_url@branch_name`. For example, "https://example.com/llama_deploy.git@branch_name".
            destination: The path in the local filesystem where to clone the git repository.
        """
        pass

    @staticmethod
    def _parse_source(source: str) -> tuple[str, str | None]:
        pass
