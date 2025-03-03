from src.db.sessions import get_db
from src.db.models.user import User
# from db.models.extracurricular_event import ExtracurricularEvent
from src.db.models.feedback import Feedback
from sqlalchemy import select

async def notify_new_feedback(bot, f: Feedback):
    async with get_db() as db:
        result = await db.execute(select(User).where(User.is_admin == True))
        users = result.scalars().all()

    text = f"Новая обратная связь!\n" \
           f"ID: {f.id}\nTelegram ID: {f.telegram_id}\nUsername: {f.username}\nName: {f.name}\nСообщение: {f.message}"

    for user in users:
        await bot.send_message(chat_id=user.telegram_id, text=text)
