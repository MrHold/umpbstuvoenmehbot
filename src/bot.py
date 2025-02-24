import asyncio
from aiogram import Bot, Dispatcher
from src.utils.config_loader import CONFIG
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from src.handlers.main_menu_handler import router as main_menu_router
from handlers.extracurricular_events_menu_handler import router as extracurricular_events_router
from src.handlers.subscription_handler import router as subs_router
from src.handlers.admin_handler import router as admin_router
from src.handlers.contacts_handler import router as contacts_router
from src.handlers.feedback_handler import router as feedback_router
from src.handlers.suggestions_handler import router as suggestions_router
from src.handlers.feedback_and_suggestions_handlers import router as feedback_and_suggestions_router
from src.handlers.enter_extracurricular_activities_handler import router as extracurricular_activities_router
from src.handlers.mero_menu_handler import router as mero_menu_router


async def main():
    bot = Bot(
        token=CONFIG["BOT_TOKEN"], 
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(main_menu_router)
    dp.include_router(extracurricular_events_router)
    dp.include_router(subs_router)
    dp.include_router(admin_router)
    dp.include_router(contacts_router)
    dp.include_router(feedback_router)
    dp.include_router(suggestions_router)
    dp.include_router(feedback_and_suggestions_router)
    dp.include_router(extracurricular_activities_router)
    dp.include_router(mero_menu_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
