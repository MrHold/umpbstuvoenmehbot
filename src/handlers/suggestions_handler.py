from aiogram import Router, types, F
from src.keyboards.suggestions_keyboards import suggestions_menu_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.sessions import get_db
from src.db.models.feedback import Feedback
from src.utils.suggestions_notification_utils import notify_new_suggestion
from sqlalchemy import insert, select, update


router = Router()

@router.callback_query(F.data == "enter_suggestions_menu")
async def enter_feedback_menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text("Напишите ваше предложение:", reply_markup=suggestions_menu_inline_kb())
    await state.set_state(SuggestionsForm.message)

class SuggestionsForm(StatesGroup):
    message = State()
    contact = State()


@router.message(SuggestionsForm.message)
async def save_message(message: types.Message, state: FSMContext):
    username = message.from_user.username if message.from_user.username else ""
    async with get_db() as db:
        await db.execute(insert(Feedback).values(telegram_id=message.from_user.id, name=message.from_user.full_name, username=username, type="suggestion", message=message.text))
        await db.commit()
    await state.set_state(SuggestionsForm.contact)
    await message.answer("Введите контактные данные, по которым мы сможем вам ответить:")


@router.message(SuggestionsForm.contact)
async def save_contact(message: types.Message, state: FSMContext):
    async with get_db() as db:
        last_feedback = await db.execute(select(Feedback).where(Feedback.telegram_id == message.from_user.id).order_by(Feedback.id.desc()).limit(1))
        last_feedback = last_feedback.scalar()
        await db.execute(update(Feedback).values(contact=message.text).where(Feedback.id == last_feedback.id))
        await db.commit()
        a = await db.execute(select(Feedback).where(Feedback.message == last_feedback.message))
        last_feedback = a.scalar()
    await message.answer("Спасибо за предложение!", reply_markup=suggestions_menu_inline_kb())
    await state.clear()
    await notify_new_suggestion(message.bot, last_feedback)