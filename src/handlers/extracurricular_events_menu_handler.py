from aiogram import Router, types, F
from aiogram.filters import Command
from src.keyboards.events_keyboards import events_kb
from src.db.sessions import get_db
from db.models.extracurricular_event import ExtracurricularEvent
from sqlalchemy.future import select
from datetime import datetime, timedelta
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

class EventsStates(StatesGroup):
    week_offset = State()

# @router.message(F.text == "Мероприятия")
# @router.callback_query(F.data == "enter_events_menu")
# async def show_events_list(message: types.Message, state: FSMContext):
#     await state.set_state(EventsStates.week_offset)
#     await state.update_data(week_offset=0)
#     await print_events_week(message, 0)

@router.callback_query(F.data == "enter_events_menu")
async def show_events_list(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(EventsStates.week_offset)
    await state.update_data(week_offset=0)
    await print_events_week(call.message, 0)
    await call.answer()

@router.callback_query(F.data.startswith("events_week_"))
async def events_pagination(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")
    new_offset = int(data[2])
    await state.update_data(week_offset=new_offset)
    text = await get_events_week_text(new_offset)
    await call.message.edit_text(text, reply_markup=events_kb(new_offset))

async def print_events_week(message: types.Message, week_offset: int):
    text = await get_events_week_text(week_offset)
    await message.answer(text, reply_markup=events_kb(week_offset))

async def get_events_week_text(week_offset: int) -> str:
    start_of_week = datetime.now() + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=7)
    async with get_db() as db:
        result = await db.execute(
            select(ExtracurricularEvent)
            .where(ExtracurricularEvent.date >= start_of_week, ExtracurricularEvent.date < end_of_week, ExtracurricularEvent.is_active == True)
            .order_by(ExtracurricularEvent.date)
        )
        events = result.scalars().all()

    text = f"Мероприятия с {start_of_week.strftime('%d.%m.%Y')} по {end_of_week.strftime('%d.%m.%Y')}:\n"
    if not events:
        text += "Нет мероприятий на этой неделе."
    else:
        for ev in events:
            text += f"{ev.date.strftime('%d.%m %H:%M')} - {ev.title} ({ev.location})\n"
    return text
