from pydantic import BaseModel


class BaseCoin(BaseModel):
    id: str
    symbol: str
    name: str


class DescribedCoin(BaseCoin):
    current_price: float
    market_cap: float
    high_24h: float
    low_24h: float
    price_change_24h: float
    price_change_percentage_24h: float
    price_change_percentage_1h_in_currency: float
