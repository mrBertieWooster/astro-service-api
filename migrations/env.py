from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from app.config import settings
from app.api.v1.models.horoscope import Base

# метаданные моделей
target_metadata = Base.metadata

config = context.config
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# Настройка логгирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()