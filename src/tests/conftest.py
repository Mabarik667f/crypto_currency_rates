import pytest
from core import init_db, settings
from fastapi.testclient import TestClient
from main import app
from loguru import logger


@pytest.fixture(scope="function")
async def mongo_test_data():
    settings.MONGO_INITDB_DATABASE="test_db"
    client, db = await init_db()
    yield client, db


@pytest.fixture(scope="function")
async def client(mongo_test_data):
    client, db = mongo_test_data
    app.client = client #type: ignore[attr-defined]
    app.db = db #type: ignore[attr-defined]
    return TestClient(app)
