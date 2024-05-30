"""
Data access object - интерфейс для взаимодействия с базой данных.
"""

from typing import Any, Optional

from sqlalchemy import Delete, Insert, Select, Update, delete, insert, select, update

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
    async def find_by_id(cls, id) -> Optional[Any]:
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
            query: Select = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def get_one_or_none(cls, filter_by: dict) -> Optional[Any]:
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
        result.scalars().one() : DAO.model
            обьект атрибута model
        None
        """
        async with async_session_maker() as session:
            query: Select = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def get_all(cls, filter_by: dict) -> list:
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
        objects : List[DAO.model]
            список обьектов атрибута model
        """
        async with async_session_maker() as session:
            query: Select = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return [row[0] for row in result.fetchall()]

    @classmethod
    async def add(cls, data: dict) -> Optional[Any]:
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
        None
        """
        async with async_session_maker() as session:
            query: Insert = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def update(cls, filter_by: dict, data: dict) -> list:
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
        None
        """

        async with async_session_maker() as session:
            query: Update = (
                update(cls.model)
                .filter_by(**filter_by)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(query)

            await session.commit()
            return [row[0] for row in result.fetchall()]

    @classmethod
    async def delete(cls, filter_by: dict) -> list:
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

        """
        async with async_session_maker() as session:
            query: Delete = (
                delete(cls.model).filter_by(**filter_by).returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return [row[0] for row in result.fetchall()]
