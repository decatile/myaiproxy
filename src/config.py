from typing import Any

from pydantic_settings import BaseSettings, YamlConfigSettingsSource, SettingsConfigDict, PydanticBaseSettingsSource


class CORSSettings(BaseSettings):
    allowed_origins: list[str] = []


class PluginSettings(BaseSettings):
    name: str
    config: dict[str, Any]


class ProfileSettings(BaseSettings):
    type Plugins = list[PluginSettings]

    prefix: str
    plugins: Plugins


class Settings(BaseSettings):
    type Profiles = list[ProfileSettings]

    cors: CORSSettings = CORSSettings()
    profiles: Profiles = []

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
