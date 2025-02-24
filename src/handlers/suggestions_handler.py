from aiogram import Router, types, F
from src.keyboards.suggestions_keyboards import suggestions_menu_inline_kb

router = Router()

@router.callback_query(F.data == "enter_suggestions_menu")
async def enter_feedback_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("Предложения:", reply_markup=suggestions_menu_inline_kb())