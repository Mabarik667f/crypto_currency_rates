from accounts.crud import create_user


async def test_create_user(mongo_test_data):
    client, db = mongo_test_data
    user_id = 1
    cur_len = await db.accounts.count_documents({})
    await create_user(db, user_id)
    assert cur_len + 1 == await db.accounts.count_documents({})
    await create_user(db, user_id)
    assert cur_len + 1 == await db.accounts.count_documents({})
