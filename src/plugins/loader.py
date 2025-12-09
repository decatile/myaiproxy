from typing import Any, cast
from importlib import import_module

from pydantic_settings import BaseSettings

from src.config import ProfileSettings
from src.plugins.pipeline import PluginPipeline
from src.utils.logger import get_logger
from src.plugins.abc import BasePlugin, AbstractPlugin

log = get_logger(__name__)


def load_plugin(name: str, settings: dict[str, Any]) -> AbstractPlugin:
    log.info(f'({name}) Loading plugin...')
    module = import_module(name)

    log.debug(f'({name}) Verifying classes...')
    assert issubclass(module.Plugin, BasePlugin), 'Should derive from AbstractPlugin'
    assert issubclass(module.Settings, BaseSettings), 'Should derive from BaseSettings'

    log.debug(f'({name}) Reading settings...')
    settings = module.Settings(**settings)

    log.debug(f'({name}) Instantiating class...')
    plugin = module.Plugin(settings)

    log.debug(f'({name}) Successfully initialized!')
    return cast(BasePlugin[BaseSettings], plugin)


def load_pipeline_for_profile(profile: ProfileSettings) -> AbstractPlugin:
    result = []

    for plugin in profile.plugins:
        result.append(load_plugin(plugin.name, plugin.config))

    return PluginPipeline(result)
