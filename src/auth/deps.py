from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth.exceptions import TelegramAuthError
from .schemas import TelegramHash

security = HTTPBearer()
AuthDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]


# mock realisation
def check_auth(hash: TelegramHash) -> TelegramHash:
    if hash.hash != "1111":
        raise TelegramAuthError(field="hash", msg="Auth error")
    return hash


TGCheckDep = Annotated[TelegramHash, Depends(check_auth)]
