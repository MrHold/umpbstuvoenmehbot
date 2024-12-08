import asyncio
from aiogram import Bot, Dispatcher
from src.utils.config_loader import CONFIG
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from src.handlers.main_menu_handler import router as main_menu_router
from src.handlers.org_menu_handler import router as org_router
from src.handlers.events_menu_handler import router as events_router
from src.handlers.subscription_handler import router as subs_router
from src.handlers.admin_handler import router as admin_router
from src.handlers.contacts_handler import router as contacts_router


async def main():
    bot = Bot(
        token=CONFIG["BOT_TOKEN"], 
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(main_menu_router)
    dp.include_router(org_router)
    dp.include_router(events_router)
    dp.include_router(subs_router)
    dp.include_router(admin_router)
    dp.include_router(contacts_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
