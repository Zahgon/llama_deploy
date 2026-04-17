import asyncio
import inspect
from typing import Any, AsyncGenerator, Callable, Generic, TypeVar

from asgiref.sync import async_to_sync
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from typing_extensions import ParamSpec

from llama_deploy.client.base import _BaseClient


class _Base(BaseModel):
    """The base model provides fields and functionalities common to derived models and collections."""

    client: _BaseClient = Field(exclude=True)
    _instance_is_sync: bool = PrivateAttr(default=False)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _prepare(self, _class: type) -> type:
        pass


T = TypeVar("T", bound=_Base)


class Model(_Base):
    id: str


class Collection(_Base, Generic[T]):
    """A generic container of items of the same model type."""

    items: dict[str, T]

    def get(self, id: str) -> T:
        """Returns an item from the collection."""
        return self.items[id]

    async def list(self) -> list[T]:
        """Returns a list of all the items in the collection."""
        pass


# Generic type for what's returned by the async generator
_G = TypeVar("_G")
# Generic parameter for the wrapped generator method
_P = ParamSpec("_P")
# Generic parameter for the wrapped generator method return value
_R = TypeVar("_R")


async def _async_gen_to_list(async_gen: AsyncGenerator[_G, None]) -> list[_G]:
    pass


def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""
    pass
