from src.db.sessions import get_db
from src.db.models.user import User
from db.models.extracurricular_event import ExtracurricularEvent
from sqlalchemy import select

async def notify_new_event(bot, event: ExtracurricularEvent):
    # Выбираем всех пользователей, у которых is_subscribed_for_events = True
    async with get_db() as db:
        result = await db.execute(select(User).where(User.is_subscribed_for_events == True))
        users = result.scalars().all()

    text = f"Новое мероприятие!\n" \
           f"{event.title}\n" \
           f"{event.date.strftime('%d.%m %H:%M')}\n{event.location}\n" \
           f"{event.description}"

    for user in users:
        await bot.send_message(chat_id=user.telegram_id, text=text)
