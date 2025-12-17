from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from pydantic_settings import BaseSettings

from src.utils.logger import get_logger_by_class


class PluginContext(BaseModel):
    headers: dict[str, Any]
    body: dict[str, Any]


class AbstractPlugin(ABC):
    @abstractmethod
    async def process(self, ctx: PluginContext) -> None:
        ...


class BasePlugin[T: BaseSettings](AbstractPlugin, ABC):
    def __init__(self, settings: T):
        self.settings = settings
        self.logger = get_logger_by_class(self.__class__)
