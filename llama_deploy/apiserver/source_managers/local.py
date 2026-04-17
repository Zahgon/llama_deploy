import shutil
from pathlib import Path

from .base import SourceManager, SyncPolicy


class LocalSourceManager(SourceManager):
    """A SourceManager specialized for sources of type `local`."""

    def sync(
        self,
        source: str,
        destination: str | None = None,
        sync_policy: SyncPolicy = SyncPolicy.REPLACE,
    ) -> None:
        """Copies the folder with path `source` into a local path `destination`.

        Args:
            source: The filesystem path to the folder containing the source code.
            destination: The path in the local filesystem where to copy the source directory.
        """
        pass

    def relative_path(self, source: str) -> str:
        pass
