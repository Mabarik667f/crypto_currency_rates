from pydantic import Field
from pydantic.main import BaseModel


class AddObserveCoins(BaseModel):
    coins_ids: list[str] = Field(max_length=10)
