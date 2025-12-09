from typing import AsyncGenerator, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient

from src.config import settings
from src.utils.logger import get_logger
from src.web.endpoints import define_for_profile

from contextlib import asynccontextmanager


@asynccontextmanager
async def stateful_lifespan(_app: FastAPI) -> AsyncGenerator[dict[str, Any]]:
    async with AsyncClient() as http_client:
        yield {'http_client': http_client}


def create_app() -> FastAPI:
    log = get_logger(__name__)

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
        log.info(f'Setting up profile with prefix "{profile.prefix}"')
        define_for_profile(app, profile)

    return app


app = create_app()
