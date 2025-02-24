from src.db.sessions import get_db
from src.db.models.user import User
# from db.models.extracurricular_event import ExtracurricularEvent
from db.models.meros import Mero
from sqlalchemy import select

async def notify_new_mero(bot, mero: Mero):
    # Выбираем всех пользователей, у которых is_subscribed_for_events = True
    async with get_db() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()

    text = f"Новое мероприятие!\n" \
           f"{mero.title}\n" \
           f"{mero.date.strftime('%d.%m %H:%M')}\n{mero.location}\n" \
           f"{mero.description}"

    for user in users:
        await bot.send_message(chat_id=user.telegram_id, text=text)
