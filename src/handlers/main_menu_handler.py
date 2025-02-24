from aiogram import Router, types, F
from aiogram.filters import Command
from src.db.sessions import get_db
from src.db.models.user import User
from sqlalchemy import select
from src.utils.config_loader import CONFIG
from src.keyboards.main_menu_keyboards import main_menu_inline_kb

router = Router()

@router.message(Command("start"))
async def show_main_menu(message: types.Message):
    async with get_db() as db:
        result = await db.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar()
        if not user:
            new_user = User(telegram_id=message.from_user.id, username=message.from_user.username, name=message.from_user.full_name)
            if message.from_user.id in CONFIG["ADMINS"]:
                new_user.is_admin = True
            db.add(new_user)
            await db.commit()
            user = new_user
        else:
            if message.from_user.id in CONFIG["ADMINS"] and not user.is_admin:
                user.is_admin = True
                await db.commit()

    kb = main_menu_inline_kb(is_admin=user.is_admin)
    # kb = main_menu_inline_kb(is_admin=False)
    await message.answer("Главное меню:", reply_markup=kb)

@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(call: types.CallbackQuery):
    async with get_db() as db:
        result = await db.execute(select(User).where(User.telegram_id == call.from_user.id))
        user = result.scalar()

    kb = main_menu_inline_kb(is_admin=user.is_admin)
    await call.message.edit_text("Главное меню:", reply_markup=kb)
    await call.answer()
