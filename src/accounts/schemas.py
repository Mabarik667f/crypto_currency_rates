from cryptowrapper.schemas import BaseCoin
from pydantic import BaseModel


class MongoUser(BaseModel):
    user_id: str
    observedCoins: list[BaseCoin]

    @staticmethod
    def serializer(user_data: dict) -> "MongoUser":
        observedCoins = (
            user_data["observedCoins"]
            if user_data.get("observedCoins") is not None
            else []
        )
        return MongoUser(user_id=user_data["user_id"], observedCoins=observedCoins)
