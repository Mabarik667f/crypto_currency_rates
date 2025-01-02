from httpx import AsyncClient
from loguru import logger


async def test_auth(client: AsyncClient):
    response = await client.post("/accounts/auth/telegram")
    assert response.status_code == 201

    response = await client.post("/accounts/auth/telegram")
    assert response.status_code == 201
