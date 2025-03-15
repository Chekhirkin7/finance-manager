from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from fastapi_app.database import DATABASE_URL
from fastapi_app.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "+psycopg2")

connectable = create_engine(SYNC_DATABASE_URL, poolclass=pool.NullPool)


def run_migrations_offline() -> None:
    context.configure(
        url=SYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
