from cryptowrapper.crud import insert_coins


async def test_insert_coins(mongo_test_data):
    client, db = mongo_test_data
    test_data = [{"id": i} for i in range(500)]
    await insert_coins(db, test_data)  # type: ignore
    count = await db.coins.count_documents({})
    assert count == 500
