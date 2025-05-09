import json
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from app.core.settings import Settings

security = HTTPBasic()


class BasicAuth:
    settings = Settings()

    def __init__(self, credentials: HTTPBasicCredentials):
        self.__credentials = credentials

        with open(self.settings.credentials_path) as credentials_file:
            self.__users_credentials = json.load(credentials_file)

    def validate_user(self) -> str:
        user_credential = self.__users_credentials.get(self.__credentials.username)

        if not user_credential or user_credential["password"] != self.__credentials.password:
            raise HTTPException(
                detail="Incorrect username or password.",
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Basic"},
            )

        return self.__credentials.username


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return BasicAuth(credentials).validate_user()
