# src/db/migrations/env.py
import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Добавляем путь к проекту для импорта моделей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Импортируйте ваши модели здесь
from src.db.models.user import User
from src.db.models.extracurricular_event import ExtracurricularEvent
from src.db.models.feedback import Feedback
from src.db.models.meros import Mero
from src.db.models.schedule import Schedule  # Импортируйте модель Schedule
from src.db.models.groups import Group  # Импортируйте модель Group
# Импортируйте другие модели при необходимости

# Получаем конфигурацию Alembic
config = context.config

# Читаем конфигурацию логирования
fileConfig(config.config_file_name)

# Указываем метаданные для автогенерации
target_metadata = [User.metadata, ExtracurricularEvent.metadata, Mero.metadata, Feedback.metadata, Schedule.metadata, Group.metadata]  # Добавьте все метаданные ваших моделей

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Включаем сравнение типов
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Включаем сравнение типов
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
