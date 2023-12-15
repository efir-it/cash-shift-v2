from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс настроек

    Атрибуты
    --------
    DB_HOST: str
        адрес хоста сервера
    DB_PORT: int
        порт
    DB_USER: str
        имя пользователя
    DB_PASS: str
        пароль пользователя
    DB_NAME: str
        имя базы данных

    RABBITMQ_HOST: str
        адрес хоста RABBITMQ
    RABBITMQ_PORT: str
        порт RABBITMQ
    RABBITMQ_USER: str
        имя пользователя RABBITMQ
    RABBITMQ_PASS: str
        пароль пользователя RABBITMQ

    TOKEN_OWNER_KEY: str
        секретный ключ owner
    TOKEN_WORKER_KEY: str
        секретный ключ worker
    TOKEN_OWNER_AUDIENCE: str
        ...
    TOKEN_WORKER_AUDIENCE: str
        ...
    TOKEN_ISSUER: str
        ...
    ALGORITHM: str
        алгоритм шифрования токенов

    MODE: Literal["DEV", "TEST", "PROD"]  # default DEV, test activating for start tests
        режим запуска
    LOG_LEVEL: str
        режим логгирования
    """

    model_config = SettingsConfigDict(env_file=".env")

    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASS: str

    TOKEN_OWNER_KEY: str
    TOKEN_WORKER_KEY: str
    TOKEN_OWNER_AUDIENCE: str
    TOKEN_WORKER_AUDIENCE: str
    TOKEN_ISSUER: str
    ALGORITHM: str

    TEST_DB_HOST: Optional[str] = None
    TEST_DB_PORT: Optional[int] = None
    TEST_DB_USER: Optional[str] = None
    TEST_DB_PASS: Optional[str] = None
    TEST_DB_NAME: Optional[str] = None

    TEST_OWNER_TOKEN: Optional[str] = None
    TEST_WORKER_TOKEN: Optional[str] = None
    TEST_OWNER_ID: Optional[str] = None
    TEST_ORGANIZATION_ID: Optional[str] = None
    TEST_WORKER_ID: Optional[str] = None
    TEST_TIMEDELTA: Optional[int] = None

    ORIGINS: str


settings = Settings()
