from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from app.config import settings
from app.api.v1.models.horoscope import Base

# метаданные моделей
target_metadata = Base.metadata

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("+asyncpg", ""))

# Логи
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    
def get_database_url():
    return settings.DATABASE_URL.replace("+asyncpg", "")

def run_migrations_offline():
    """Выполнение миграций в offline-режиме."""
    context.configure(
        url=get_database_url(),
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Выполнение миграций в online-режиме."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url() 

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()