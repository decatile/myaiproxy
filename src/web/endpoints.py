from typing import Any, AsyncGenerator

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse
from httpx import AsyncClient

from src.config import ProfileSettings
from src.plugins.abc import PluginContext
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

        if r.status_code != 200:
            raise HTTPException(r.status_code, {'error': r.text})

        return r.json()

    @app.post(f'/{profile.prefix}/v1/chat/completions')
    async def completions(
            request: Request,
            client: AsyncClient = Depends(get_http_client)
    ) -> StreamingResponse:
        ctx = PluginContext(headers=dict(request.headers), body=await request.json())

        try:
            await pipeline.process(ctx)
        except Exception as e:
            log.exception('Failed to process pipeline')
            raise HTTPException(500, {'error': str(e)})

        r = await client.post(
            f'{profile.base_url}/v1/chat/completions',
            headers=ctx.headers,
            json=ctx.body
        )

        if r.status_code != 200:
            raise HTTPException(r.status_code, {'error': r.text})

        async def create_stream() -> AsyncGenerator[bytes]:
            async for chunk in r.aiter_bytes():
                yield chunk

        return StreamingResponse(
            create_stream(),
            headers=r.headers
        )
