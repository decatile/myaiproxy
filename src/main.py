from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings


def create_app() -> FastAPI:
    # noinspection PyShadowingNames
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return app


app = create_app()
