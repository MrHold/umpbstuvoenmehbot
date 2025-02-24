from aiogram import Router, types, F
from src.keyboards.events_menu_keyboards import events_menu_inline_kb
from src.keyboards.timeline_keyboards import timeline_menu_inline_kb

router = Router()

@router.callback_query(F.data == "enter_events_menu")
async def enter_events_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Расписание мероприятий:", reply_markup=events_menu_inline_kb())

@router.callback_query(F.data.in_({"enter_career_mero_menu", "enter_science_mero_menu", "enter_civic_mero_menu", "enter_cultural_mero_menu", "enter_sport_mero_menu", "enter_all_mero_menu"}))
async def enter_events_submenu(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Расписание мероприятий:", reply_markup=timeline_menu_inline_kb())