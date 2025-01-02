import asyncio
from fastapi.requests import Request
import pytest
from core import init_db, settings
from httpx import ASGITransport, AsyncClient
from main import app
from loguru import logger


@pytest.fixture(scope="function")
async def mongo_test_data():
    settings.MONGO_INITDB_DATABASE = "test_db"
    client, db = await init_db()
    yield client, db
    await client.drop_database("test_db")
    client.close()


@pytest.fixture(scope="function")
async def client(mongo_test_data):
    client, db = mongo_test_data
    app.client = client  # type: ignore[attr-defined]
    app.db = db  # type: ignore[attr-defined]
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
