from typing import AsyncGenerator, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient

from src.config import settings
from src.utils.logger import get_logger
from src.web.endpoints import router_for_profile

from contextlib import asynccontextmanager

log = get_logger(__name__)


@asynccontextmanager
async def stateful_lifespan(_app: FastAPI) -> AsyncGenerator[dict[str, Any]]:
    async with AsyncClient() as http_client:
        yield {'http_client': http_client}


def create_app() -> FastAPI:
    # noinspection PyShadowingNames
    app = FastAPI(lifespan=stateful_lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    for profile in settings.profiles:
        app.include_router(router_for_profile(profile))

    return app


app = create_app()
