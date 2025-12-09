from abc import ABC, abstractmethod
from typing import Any

from pydantic_settings import BaseSettings


class AbstractPlugin[T: BaseSettings](ABC):
    def __init__(self, settings: T):
        self.settings = settings

    @abstractmethod
    def process(self, body: dict[str, Any]) -> dict[str, Any]: ...

    @staticmethod
    @abstractmethod
    def settings_cls() -> type[T]: ...
