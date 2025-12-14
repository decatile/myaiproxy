from typing import Any

from pydantic_settings import BaseSettings

from src.plugins.abc import BasePlugin, PluginContext


class Settings(BaseSettings):
    body: dict[str, Any] = {}
    headers: dict[str, Any] = {}


class Plugin(BasePlugin[Settings]):
    async def process(self, ctx: PluginContext) -> None:
        for k, v in self.settings.body.items():
            ctx.body[k] = v
        for k, v in self.settings.headers.items():
            ctx.headers[k] = v

#
# Заметьте, что 'Settings' и 'Plugin' - имеют специальное значение в плагинах!
# Они должны экспортировать именно эти имена.
#
