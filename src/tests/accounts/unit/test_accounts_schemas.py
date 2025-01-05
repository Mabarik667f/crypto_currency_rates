from accounts.schemas import MongoUser
from cryptowrapper.schemas import BaseCoin

def test_mongo_user_schema():
    coins = [
        BaseCoin(id=str(i), symbol=str(i), name=str(i))
        for i in range(3)
    ]
    user_data = {"user_id": "111", "observed_coins": coins}
    user= MongoUser.serializer(user_data)
    assert isinstance(user.observed_coins[0], BaseCoin)
