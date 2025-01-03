from auth.schemas import TokenData
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from loguru import logger

hash = "1111"


async def test_auth(client: AsyncClient):
    data = {"hash": hash, "user_id": "100"}
    response = await client.post("/auth/telegram", json=data)
    assert response.status_code == 200
    assert response.json().get("access") is not None
    assert response.json().get("refresh") is not None

    data["hash"] = "dsadadad"
    response = await client.post("/auth/telegram", json=data)
    assert response.status_code == 400
    assert response.json().get("access") is None
    assert response.json().get("refresh") is None


async def test_refresh(
    get_user_data: tuple[AsyncIOMotorDatabase, TokenData], client: AsyncClient
):
    _, tokens = get_user_data
    headers = {"Authorization": f"Bearer {tokens.access}"}
    data = {"refresh": tokens.refresh}

    response = await client.post("/auth/refresh", json=data, headers=headers)
    assert response.status_code == 201
    assert (
        response.json().get("access") is not None
        and response.json().get("refresh") is not None
    )

    response = await client.post("/auth/refresh", json=data, headers={})
    assert response.status_code == 403
