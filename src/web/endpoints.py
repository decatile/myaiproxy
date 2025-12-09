from typing import Any, AsyncGenerator

from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from httpx import AsyncClient

from src.config import ProfileSettings
from src.plugins.loader import load_pipeline_for_profile
from src.utils.logger import get_logger
from src.web.di import get_http_client

log = get_logger(__name__)


def define_for_profile(app: FastAPI, profile: ProfileSettings) -> None:
    pipeline = load_pipeline_for_profile(profile)

    log.info(f'Defining /{profile.prefix}/v1/models')
    log.info(f'Defining /{profile.prefix}/v1/chat/completions')

    @app.get(f'/{profile.prefix}/v1/models')
    async def models(client: AsyncClient = Depends(get_http_client)) -> Any:
        r = await client.get(f'{profile.base_url}/v1/models')
        r.raise_for_status()
        return r.json()

    @app.post(f'/{profile.prefix}/v1/chat/completions')
    async def completions(body: dict[str, Any], client: AsyncClient = Depends(get_http_client)) -> StreamingResponse:
        r = await client.post(
            f'{profile.base_url}/v1/chat/completions',
            json=pipeline.process(body)
        )
        r.raise_for_status()

        async def create_stream() -> AsyncGenerator[bytes]:
            async for chunk in r.aiter_bytes():
                yield chunk

        return StreamingResponse(
            create_stream(),
            headers=r.headers
        )
