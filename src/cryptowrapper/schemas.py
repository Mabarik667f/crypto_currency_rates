from pydantic import BaseModel


class BaseCoin(BaseModel):
    id: str
    symbol: str
    name: str
