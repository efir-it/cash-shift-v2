from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Класс настроек
    """
    MODE: Literal['DEV', 'TEST', 'PROD']  # default DEV, test activating for start tests
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

    class Config:
        """
        Путь к файлу со скрытыми данными для подключения и тестирование бд
        """
        env_file = '.env'
        orm_mode = True


settings = Settings()


