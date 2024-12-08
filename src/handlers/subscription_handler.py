from aiogram import Router, types, F
from src.keyboards.subscription_keyboards import subscription_kb
from src.db.models.user import User
from src.db.sessions import get_db
from aiogram.filters import Command
from sqlalchemy import update, select

router = Router()

# @router.message(F.text == "Уведомления")
# @router.callback_query(F.data == "enter_subs_menu")
# async def subscription_menu(message: types.Message):
#     await message.answer("Настройка уведомлений:", reply_markup=subscription_kb())

@router.callback_query(F.data == "enter_subs_menu")
async def subscription_menu(callback: types.CallbackQuery):
    await callback.message.answer("Настройка уведомлений:", reply_markup=subscription_kb())

@router.callback_query(F.data.in_({"subscribe", "unsubscribe"}))
async def change_subscription(callback: types.CallbackQuery):
    subscribe = (callback.data == "subscribe")
    async with get_db() as db:
        await db.execute(
            update(User)
            .where(User.telegram_id == callback.from_user.id)
            .values(is_subscribed_for_events=subscribe)
        )
        await db.commit()
    await callback.message.answer("Настройки обновлены!")
    await callback.answer()
