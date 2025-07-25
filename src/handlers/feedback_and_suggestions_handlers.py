from aiogram import Router, types, F
from src.keyboards.feedback_and_suggestions_menu_keyboards import feedback_menu_inline_kb

router = Router()

# @router.message(F.text == "Обратная связь и предложения")
@router.callback_query(F.data == "enter_feedback_and_suggestions_menu")
async def enter_feedback_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("Обратная связь и предложения:", reply_markup=feedback_menu_inline_kb())