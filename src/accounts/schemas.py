from cryptowrapper.schemas import BaseCoin
from pydantic import BaseModel


class MongoBaseUser(BaseModel):
    user_id: str


class MongoUser(MongoBaseUser):
    observed_coins: list[BaseCoin]

    @staticmethod
    def serializer(user_data: dict) -> "MongoUser":
        observed_coins = (
            user_data["observed_coins"]
            if user_data.get("observed_coins") is not None
            else []
        )
        return MongoUser(user_id=user_data["user_id"], observed_coins=observed_coins)
