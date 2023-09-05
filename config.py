from typing import Literal

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

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    

    class Config:
        """
        Путь к файлу со скрытыми данными для подключения и тестирование бд.
        """

        env_file = ".env"
        from_attributes = True


settings = Settings()
