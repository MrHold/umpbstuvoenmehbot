from aiogram import Router, types, F
from src.keyboards.feedback_keyboards import feedback_menu_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.db.sessions import get_db
from src.db.models.feedback import Feedback
from sqlalchemy import insert, select
from src.utils.feedback_notification_utils import notify_new_feedback

router = Router()

@router.callback_query(F.data == "enter_feedback_menu")
async def enter_feedback_menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text("Напишите вашу обратную связь:", reply_markup=feedback_menu_inline_kb())
    await state.set_state(FeedbackForm.message)

class FeedbackForm(StatesGroup):
    message = State()

@router.message(FeedbackForm.message)
async def save_message(message: types.Message, state: FSMContext):
    username = message.from_user.username if message.from_user.username else ""
    async with get_db() as db:
        await db.execute(insert(Feedback).values(telegram_id=message.from_user.id, name=message.from_user.full_name, username=username, type="feedback", message=message.text))
        await db.commit()
        a = await db.execute(select(Feedback).where(Feedback.message == message.text))
        feedback = a.scalar()
    await message.answer("Спасибо за обратную связь!", reply_markup=feedback_menu_inline_kb())
    await state.clear()
    await notify_new_feedback(message.bot, feedback)
    