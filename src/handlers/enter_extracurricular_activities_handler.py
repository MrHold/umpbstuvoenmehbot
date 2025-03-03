from aiogram import Router, types, F
from src.keyboards.extracurricular_activities_keyboards import extracurricular_activities_menu_inline_kb
from src.db.sessions import get_db
from db.models.extracurricular_event import ExtracurricularEvent
from sqlalchemy import select, delete, insert, update

router = Router()

@router.callback_query(F.data == "enter_extracurricular_activities_menu")
async def enter_extracurricular_activities_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Расписание внеучебных занятий:", reply_markup=extracurricular_activities_menu_inline_kb())

@router.callback_query(F.data == "enter_tssk_menu")
async def enter_tssk_menu(call: types.CallbackQuery):
    await call.answer()
    text = "Творческие секции, студии, клубы"
    async with get_db() as db:
        result = await db.execute(select(ExtracurricularEvent).where(ExtracurricularEvent.id == 1))
        events = result.scalars().all()
    if events:
        text += f"\n\n{events[0].message}"
    await call.message.answer(text=text)

@router.callback_query(F.data == "enter_sssk_menu")
async def enter_sssk_menu(call: types.CallbackQuery):
    await call.answer()
    text = "Спортивные секции и сборные команды"
    async with get_db() as db:
        result = await db.execute(select(ExtracurricularEvent).where(ExtracurricularEvent.id == 2))
        events = result.scalars().all()
    if events:
        text += f"\n\n{events[0].message}"
    await call.message.answer(text=text)