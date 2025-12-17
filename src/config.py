from typing import Any

from pydantic_settings import BaseSettings, YamlConfigSettingsSource, SettingsConfigDict, PydanticBaseSettingsSource


class CORSSettings(BaseSettings):
    allowed_origins: list[str] = []


class PluginSettings(BaseSettings):
    name: str
    config: dict[str, Any]


class ProfileSettings(BaseSettings):
    prefix: str
    api_url: str
    plugins: list[PluginSettings]


class Settings(BaseSettings):
    log: dict[str, Any] = {}
    cors: CORSSettings = CORSSettings()
    profiles: list[ProfileSettings] = []

    model_config = SettingsConfigDict(yaml_file='config.yaml')

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


settings = Settings()
