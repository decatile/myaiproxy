from typing import Any, AsyncGenerator

from fastapi import Depends, Request, HTTPException, APIRouter
from fastapi.responses import StreamingResponse
from httpx import AsyncClient

from src.config import ProfileSettings
from src.plugins.abc import PluginContext, AbstractPlugin
from src.plugins.loader import load_pipeline_for_profile
from src.utils.logger import get_logger
from src.web.di import get_http_client

log = get_logger(__name__)


def router_for_profile(profile: ProfileSettings) -> APIRouter:
    router = APIRouter(prefix=f'/{profile.prefix}')
    define_endpoint_set(
        router,
        profile.api_url,
        load_pipeline_for_profile(profile)
    )
    return router


def define_endpoint_set(router: APIRouter, base_url: str, pipeline: AbstractPlugin) -> None:
    @router.get('/v1/models')
    async def models(client: AsyncClient = Depends(get_http_client)) -> Any:
        r = await client.get(f'{base_url}/v1/models')

        if r.status_code != 200:
            raise HTTPException(r.status_code, {'error': r.text})

        return r.json()

    @router.post('/v1/chat/completions')
    async def completions(
            request: Request,
            client: AsyncClient = Depends(get_http_client)
    ) -> StreamingResponse:
        ctx = PluginContext(headers=dict(request.headers), body=await request.json())

        try:
            await pipeline.process(ctx)
        except HTTPException:
            raise
        except Exception as e:
            log.exception('Failed to process pipeline')
            raise HTTPException(500, {'error': str(e)})

        r = await client.post(
            f'{base_url}/v1/chat/completions',
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
