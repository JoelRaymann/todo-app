from pydantic import BaseSettings, AnyHttpUrl
from decouple import config

from typing import List


class Settings(BaseSettings):
    '''
    A Class to handle the FASTAPI settings
    '''
    # ------- API VERSION ------------
    API_V1_STRING: str = '/api/v1'

    # ------- JWT SETTINGS -----------
    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY', cast=str)
    JWT_REFRESH_SECRET_KEY: str = config('JWT_REFRESH_SECRET_KEY', cast=str)
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRATION_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRATION_MINUTES: int = 60

    # ------- CORS ORIGIN ------------
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # ------- PROJECT META INFO ------
    PROJECT_NAME: str = 'TODO-LIST'

    # ------- DATABASE SETTINGS ------
    MONGODB_CONNECTION_STRING: str = config(
        'MONGODB_CONNECTION_STRING',
        cast=str
    )

    class Config:
        case_sensitive = True


settings = Settings()
