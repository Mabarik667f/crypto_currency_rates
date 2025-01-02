from core.exceptions import BaseError


class CoinApiError(BaseError):
    pass


class CoinNotFoundError(BaseError):
    pass
