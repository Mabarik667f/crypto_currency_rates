from httpx import AsyncClient
from loguru import logger


async def test_set_coins(client: AsyncClient):
    response = await client.post("/cryptowrapper/coins")
    body = response.json()
    assert response.status_code == 201
    assert body["coins"] >= 16000

    response = await client.post("/cryptowrapper/coins")
    second_body = response.json()
    assert response.status_code == 201
    assert (
        second_body["coins"] >= 16000
        and abs(second_body["coins"] - body["coins"]) <= 200
    )
