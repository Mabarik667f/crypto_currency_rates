from loguru import logger
async def test_base(client):
    logger.info(client.app.db)
    assert 2 + 2 == 4
