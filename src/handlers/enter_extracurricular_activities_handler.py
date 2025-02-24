from aiogram import Router, types, F
from src.keyboards.extracurricular_activities_keyboards import extracurricular_activities_menu_inline_kb

router = Router()

@router.callback_query(F.data == "enter_extracurricular_activities_menu")
async def enter_extracurricular_activities_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Расписание внеучебных занятий:", reply_markup=extracurricular_activities_menu_inline_kb())