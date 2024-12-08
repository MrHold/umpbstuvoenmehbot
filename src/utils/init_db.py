# src/init_db.py

import asyncio
from src.db.sessions import get_db
from src.db.models.user import User
from src.utils.config_loader import CONFIG
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

async def init_admins():
    async with get_db() as db:
        admin_ids = CONFIG["ADMINS"]  # Предполагается, что ADMINS - список int
        for admin_id in admin_ids:
            result = await db.execute(select(User).where(User.telegram_id == admin_id))
            user = result.scalar()
            if not user:
                new_user = User(
                    telegram_id=admin_id,
                    is_subscribed_for_events=True,
                    is_admin=True
                )
                db.add(new_user)
                try:
                    await db.commit()
                    print(f"Админ с Telegram ID {admin_id} добавлен.")
                except IntegrityError:
                    await db.rollback()
                    print(f"Ошибка при добавлении админа с Telegram ID {admin_id}.")

if __name__ == "__main__":
    asyncio.run(init_admins())
