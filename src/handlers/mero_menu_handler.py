from aiogram import Router, types, F
from src.keyboards.mero_menu_keyboards import mero_menu_inline_kb
from src.keyboards.timeline_keyboards import timeline_menu_inline_kb, back_to_timeline_menu_inline_kb
from src.db.models.meros import Mero
from sqlalchemy.future import select
from datetime import datetime, timedelta
from src.db.sessions import get_db
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

@router.callback_query(F.data == "enter_mero_menu")
async def enter_mero_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Расписание мероприятий:", reply_markup=mero_menu_inline_kb())

@router.callback_query(F.data.in_({"enter_career_mero_menu", "enter_science_mero_menu", "enter_civic_mero_menu", "enter_cultural_mero_menu", "enter_sport_mero_menu", "enter_all_mero_menu"}))
async def enter_events_submenu(call: types.CallbackQuery):
    category = call.data.split("_")[1]
    await call.answer()
    await call.message.answer("Расписание мероприятий:", reply_markup=timeline_menu_inline_kb(category))

@router.callback_query(F.data.startswith("enter_today_menu_"))
@router.callback_query(F.data.startswith("enter_week_menu_"))
@router.callback_query(F.data.startswith("enter_month_menu_"))
async def enter_events_submenu(call: types.CallbackQuery):
    data = call.data.split("_")
    timerange = data[1]
    category = data[-1]
    await call.answer()
    text = "Расписание мероприятий "
    if timerange == "today":
        text += "cегодня: \n"
        condition_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    elif timerange == "week":
        text += "на неделю: \n"
        condition_date = datetime.now() + timedelta(days=7)
    elif timerange == "month":
        text += "на месяц: \n"
        condition_date = datetime.now() + timedelta(days=30)
    async with get_db() as db:
        if category == "all":
            result = await db.execute(
                select(Mero)
                .where(Mero.is_active == True, Mero.date <= condition_date, Mero.date >= datetime.now())
                .order_by(Mero.date)
            )
            events = result.scalars().all()
            # print(events[0].date)
        else:
            result = await db.execute(
                select(Mero)
                .where(Mero.is_active == True, Mero.date <= condition_date, Mero.date >= datetime.now())
                .order_by(Mero.date)
            )
            events = result.scalars().all()
    if not events:
        text += "Нет мероприятий."
    else:
        for ev in events:
            text += f"{ev.date.strftime('%d.%m %H:%M')} - {ev.title} ({ev.location})\n"
    await call.message.edit_text(text, reply_markup=back_to_timeline_menu_inline_kb(category))
    # await call.message.answer("Расписание мероприятий:", reply_markup=back_to_main_menu())