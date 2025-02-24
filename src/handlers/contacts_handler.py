from aiogram import Router, types, F
from src.keyboards.contacts_keyboards import contacts_kb, back_to_contacts_menu_kb
from src.keyboards.main_menu_keyboards import main_menu_inline_kb

router = Router()

@router.callback_query(F.data == "enter_contacts_menu")
async def enter_contacts_menu(call: types.CallbackQuery):
    text = "Контакты:"
    await call.message.edit_text(text, reply_markup=contacts_kb())
    await call.answer()

@router.callback_query(F.data == "umpvd_contacts")
async def umpsd_contacts(call: types.CallbackQuery):
    text = "Управление молодёжной политики и студенческого досуга:\n" \
           "Почта: umpvd@voenmeh.ru\n" \
           "ВК: https://vk.com/molod_voenmeh\n"
    await call.message.edit_text(text, reply_markup=back_to_contacts_menu_kb(), link_preview_options={"is_disabled": True})
    await call.answer()

@router.callback_query(F.data == "sk_voenmeh_contacts")
async def sk_voenmeh_contacts(call: types.CallbackQuery):
    text = "Спортивный клуб «ВОЕНМЕХ»:\n" \
           "Почта: sportclub@voenmeh.ru\n" \
           "ВК: https://vk.com/sk_voenmeh\n"
    await call.message.edit_text(text, reply_markup=back_to_contacts_menu_kb(), link_preview_options={"is_disabled": True})
    await call.answer()

@router.callback_query(F.data == "cpd_contacts")
async def cpr_contacts(call: types.CallbackQuery):
    text = "Центр проектной деятельности:\n" \
           "Почта: cpr@voenmeh.ru\n" \
           "ВК: https://vk.com/projectoffice_voenmeh\n"
    await call.message.edit_text(text, reply_markup=back_to_contacts_menu_kb(), link_preview_options={"is_disabled": True})
    await call.answer()