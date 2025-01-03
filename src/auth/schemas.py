from pydantic import BaseModel


class TokenData(BaseModel):
    access: str
    refresh: str


class TokenRefresh(BaseModel):
    refresh: str


# mock realisation
class TelegramHash(BaseModel):
    hash: str
    user_id: str
