from typing import Any

from pydantic_settings import BaseSettings

from src.plugins.interface import AbstractPlugin


class Settings(BaseSettings):
    overwrite: bool
    extra: dict[str, Any]


class Plugin(AbstractPlugin[Settings]):
    def process(self, body: dict[str, Any]) -> dict[str, Any]:
        assert self.settings.overwrite, 'Currently only "overwrite: true" mode supported'
        for k, v in self.settings.extra.items():
            body[k] = v
        return body

    @staticmethod
    def settings_cls() -> type[Settings]:
        return Settings
