from aiogram import Router, types, F
from src.keyboards.contacts_keyboards import contacts_kb

router = Router()

@router.callback_query(F.data == "enter_contacts_menu")
async def enter_contacts_menu(call: types.CallbackQuery):
    text = "Контакты:\nОфис: 123456789\nEmail: info@university.com"
    await call.message.edit_text(text, reply_markup=contacts_kb())
    await call.answer()
