<p>Создание виртуальной среды: python -m venv venv</p>
<p>Активация виртуальной среды: venv\Scripts\activate</p>
<p>Установка зависимостей: python -m pip install -r requirements.txt  (или pip install -r requirements.txt)
</p>
<p>Создание миграций: alembic revision --autogenerate -m "name revisoin"</p>
<p>Применение миграций: alembic upgrade head</p>
<p>Запуск проекта: uvicorn main:app --reload</p>
<p>Запуск тестов: pytest -v -s</p>

<p>Запуск black(стиль, форматирование кода): black check/dao.py --diff --color</p>
<p>Запуск flake(ошибки в коде, не используемые переменные, и тд): flake check/dao.py</p>
<p>Запуск isort(сортировка импортов): isort main.py --diff(--diff чтобы показать разницу)</p>
<p>Запуск autoflake(не используемые импорты): autoflake main.py --diff(--diff чтобы показать разницу) в файле настроек миграций env.py нужно проставить "# noqa", по умолчанию смотрит на встроенные библиотеки python </p>