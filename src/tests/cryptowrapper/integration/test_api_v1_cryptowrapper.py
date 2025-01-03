from httpx import AsyncClient
from cryptowrapper.schemas import BaseCoin
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


async def test_search_coins(client: AsyncClient, test_coins: list[BaseCoin]):
    params = dict(query="ethereum")
    response = await client.get("/cryptowrapper/search-coins", params=params)
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]["id"] == "ethereum"
    assert response.json()[0]["name"] == "Ethereum"

    params["query"] = "ethereu"
    response = await client.get("/cryptowrapper/search-coins", params=params)
    assert response.status_code == 200
    assert len(response.json()) == 0
