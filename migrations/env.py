import os
import sys
from logging.config import fileConfig
from os.path import dirname, abspath

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import importlib.util as iu

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

# current_path = os.path.dirname(os.path.abspath(__file__))
#
# app_path = os.path.abspath(os.path.join(current_path, "..", "app"))
# sys.path.append(app_path)


from database import Base, DATABASE_URL
from check.models import Check
from check_status.models import CheckStatus
from position_check.models import PositionCheck
from type_operation.models import TypeOperation
from type_payment.models import TypePayment
from type_taxation.models import TypeTaxation
from cash_shift.models import CashShift
from event.models import Event


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", f"{DATABASE_URL}?async_fallback=True")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
