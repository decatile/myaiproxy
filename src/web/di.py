from typing import cast

from fastapi import Request
from httpx import AsyncClient


def get_http_client(request: Request) -> AsyncClient:
    return cast(AsyncClient, request.state.http_client)
