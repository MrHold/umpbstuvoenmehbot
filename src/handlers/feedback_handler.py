from aiogram import Router, types, F
from src.keyboards.feedback_keyboards import feedback_menu_inline_kb

router = Router()

@router.callback_query(F.data == "enter_feedback_menu")
async def enter_feedback_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("Обратная связь:", reply_markup=feedback_menu_inline_kb())