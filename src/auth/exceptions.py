from core.exceptions import BaseError
from jwt.exceptions import PyJWTError


class TelegramAuthError(BaseError): ...


class RefreshError(PyJWTError): ...
