from typing import Literal, Optional

from pydantic_settings import BaseSettings


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
    
    TEST_DB_HOST: str
        адрес хоста сервера тестовой бд
    TEST_DB_PORT: int
        порт тестовой бд
    TEST_DB_USER: str
        имя пользователя
    TEST_DB_PASS: str
        пароль пользователя
    TEST_DB_NAME: str
        имя тестовой базы данных

    RABBITMQ_HOST: str
        адрес хоста RABBITMQ
    RABBITMQ_PORT: str
        порт RABBITMQ
    RABBITMQ_USER: str
        имя пользователя RABBITMQ
    RABBITMQ_PASS: str
        пароль пользователя RABBITMQ

    TOKEN_CLIENT_KEY: str
        секретный ключ client
    TOKEN_WORKER_KEY: str
        секретный ключ worker
    TOKEN_CLIENT_AUDIENCE: str
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

    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: Optional[str] = None
    TEST_DB_PORT: Optional[int] = None
    TEST_DB_USER: Optional[str] = None
    TEST_DB_PASS: Optional[str] = None
    TEST_DB_NAME: Optional[str] = None

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASS: str

    TOKEN_CLIENT_KEY: str
    TOKEN_WORKER_KEY: str
    TOKEN_CLIENT_AUDIENCE: str
    TOKEN_WORKER_AUDIENCE: str
    TOKEN_ISSUER: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        from_attributes = True


settings = Settings()
