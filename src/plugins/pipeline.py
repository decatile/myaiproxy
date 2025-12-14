from src.plugins.abc import AbstractPlugin, PluginContext
from src.utils.logger import get_logger_by_class


class PluginPipeline(AbstractPlugin):
    def __init__(self, plugins: list[AbstractPlugin]) -> None:
        self.log = get_logger_by_class(PluginPipeline)
        self.plugins = plugins

    async def process(self, ctx: PluginContext) -> None:
        self.log.info('Processing request...')
        for plugin in self.plugins:
            await plugin.process(ctx)
        self.log.debug('Request successfully processed!')
