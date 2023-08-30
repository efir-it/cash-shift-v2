"""
Data access object - интерфейс для взаимодействия с базой данных.
"""

from typing import Optional
from sqlalchemy import delete, insert, select, update

from database import async_session_maker


class BaseDAO:
    """
    Базовый класс Data access object.

    Атрибуты
    --------
    model : cls
        класс реализующий модель данных

    Методы
    ------
    async def find_by_id(cls, id):
        поиск записей по ключу
    async def get_one_or_none(cls, **filter_by):
        поиск записи по параметрам
    async def get_all(cls, **filter_by):
        поиск всех записей
    async def add(cls, **data):
        добавление записи
    async def update(cls, id: int, data: dict):
        обновление записи
    async def delete(cls, id: int):
        удаление записи
    """

    model = None

    @classmethod
    async def find_by_id(cls, id) -> dict:
        """
        Возвращает обьект атрибута model (класса модели - DAO.model).

        Параметры
        ---------
        cls : cls
            Класс DAO
        id : int
            id записи в базе данных

        Возвращаемое значение
        ---------------------
        result.scalars().one() : DAO.model
            обьект атрибута model
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalars().one().__dict__

    @classmethod
    async def get_one_or_none(cls, **filter_by) -> Optional[dict]:
        """
        Возвращает обьект атрибута model (класса модели - DAO.model) или None.

        Параметры
        ---------
        cls : cls
            Класс DAO
        filter_by : dict
            параметры поиска

        Возвращаемое значение
        ---------------------
        result.__dict__ : dict
        None
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            result =  result.scalars_one_or_none()
            if result is not None:
                return result.__dict__
            else:
                return None

    @classmethod
    async def get_all(cls, **filter_by) -> list[dict]:
        """
        Возвращает список обьектов атрибута model (класса модели - DAO.model).

        Параметры
        ---------
        cls : cls
            Класс DAO
        filter_by : dict
            параметры поиска

        Возвращаемое значение
        ---------------------
        objects : List[dict]
            список обьектов атрибута model
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            objects = [row[0].__dict__ for row in result.all()]
            return objects

    @classmethod
    async def add(cls, **data) -> dict:
        """
        Добавляет в таблицу обьект атрибута model (класса модели - DAO.model).

        Параметры
        ---------
        cls : cls
            Класс DAO
        data : dict
            данные записи

        Возвращаемое значение
        ---------------------
        result: dict
        """
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.first()[0].__dict__

    @classmethod
    async def update(cls, id: int, data: dict) -> dict:
        """
        Обновляет обьект атрибута model (класса модели - DAO.model).

        Параметры
        ---------
        cls : cls
            Класс DAO
        id : int
            ключ записи
        data : dict
            данные записи

        Возвращаемое значение
        ---------------------
        result: dict
        """
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.first()[0].__dict__

    @classmethod
    async def delete(cls, id: int) -> dict:
        """
        Удаляет из таблицы обьект атрибута model (класса модели - DAO.model).

        Параметры
        ---------
        cls : cls
            Класс DAO
        id : int
            ключ записи

        Возвращаемое значение
        ---------------------
        result: dict
        """
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == id).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.first()[0].__dict__
