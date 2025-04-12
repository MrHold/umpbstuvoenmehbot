import datetime
from aiogram import Router, types
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from src.db.sessions import get_db
from db.models.schedule import Schedule
from db.models.groups import Group
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


class ScheduleStates(StatesGroup):
    group_select = State()  # выбор группы
    schedule = State()      # навигация по расписанию


def even_week(dt):
    week_number = int(dt.isocalendar()[1])
    current_month = int(dt.month)
    if current_month >= 9:
        week_number -= 35
    else:
        week_number -= 6
    return (week_number % 2 == 0)

def build_schedule_keyboard() -> InlineKeyboardMarkup:
    """
    Формирует клавиатуру для навигации: 
     - «<< Пред. день | Сегодня | След. день»
     - Переключение типа недели: «Нечётная | Чётная»
     - Быстрый выбор дня недели: «Пн | Вт | Ср | Чт | Пт»
     - Кнопки: «Назад» и «В меню»
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
          InlineKeyboardButton(text="<< Пред. день", callback_data="schedule:prev"),
          InlineKeyboardButton(text="Сегодня", callback_data="schedule:today"),
          InlineKeyboardButton(text="След. день >>", callback_data="schedule:next")
        ],
        [
          InlineKeyboardButton(text="Нечётная", callback_data="schedule:parity:Нечетная"),
          InlineKeyboardButton(text="Четная", callback_data="schedule:parity:Четная")
        ],
        [
          InlineKeyboardButton(text="Пн", callback_data="schedule:select_day:Понедельник"),
          InlineKeyboardButton(text="Вт", callback_data="schedule:select_day:Вторник"),
          InlineKeyboardButton(text="Ср", callback_data="schedule:select_day:Среда"),
          InlineKeyboardButton(text="Чт", callback_data="schedule:select_day:Четверг"),
          InlineKeyboardButton(text="Пт", callback_data="schedule:select_day:Пятница")
        ],
        [
          InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")
        ]
    ])
    return keyboard


async def send_schedule(bot, chat_id: int, state: FSMContext):
    """
    Получает данные из FSMContext, запрашивает расписание для выбранной группы
    на определённую дату и отправляет сообщение с inline-клавиатурой для навигации.
    """
    data = await state.get_data()
    group_id = data["group_id"]
    group_name = data["group_name"]
    day_offset = data.get("day_offset", 0)
    parity = data.get("parity", "Четная")
    # Вычисляем целевую дату
    target_date = datetime.date.today() + datetime.timedelta(days=day_offset)
    # Получаем название дня на русском:
    weekdays = {
       "Monday": "Понедельник",
       "Tuesday": "Вторник",
       "Wednesday": "Среда",
       "Thursday": "Четверг",
       "Friday": "Пятница",
       "Saturday": "Суббота",
       "Sunday": "Воскресенье"
    }
    current_day = weekdays.get(target_date.strftime("%A"), target_date.strftime("%A"))
    
    # Запрос расписания для выбранной группы, дня и типа недели (parity)
    async with get_db() as db:
        result = await db.execute(
            select(Schedule).where(
                Schedule.group_id == group_id,
                Schedule.day_of_week == current_day,
                Schedule.parity == parity
            )
        )
        schedule_entries = result.scalars().all()

    text = (f"Расписание для группы {group_name} на {current_day}\n"
            f"Тип недели: {parity}\n\n")
    if schedule_entries:
        for item in schedule_entries:
            time_str = item.start_time.strftime('%H:%M')
            room = "Кабинет: " + item.room if item.room else "Кабинет не указан"
            teacher = "Преподаватель: " + item.teacher if item.teacher else "Преподаватель не указан"
            text += f"{time_str} {item.subject}\n{room}, {teacher}\n\n"
    else:
        text += "Расписание отсутствует."
    await bot.send_message(chat_id, text, reply_markup=build_schedule_keyboard())


# Обработчик входа в меню расписания (вход через кнопку главного меню, а не команду)
@router.callback_query(F.data == "enter_schedule_menu")
async def schedule_menu_entry(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    # Запрашиваем группу у пользователя
    await call.message.answer("Введите, пожалуйста, название вашей группы для получения расписания:")
    await state.set_state(ScheduleStates.group_select)


# Обработчик выбора группы (пользователь вводит название группы)
@router.message(ScheduleStates.group_select)
async def process_group_selection(message: types.Message, state: FSMContext):
    group_name = message.text.strip().upper()
    async with get_db() as db:
        result = await db.execute(select(Group).where(Group.name == group_name))
        group_obj = result.scalars().first()
    if not group_obj:
        await message.answer(f"Группа {group_name} не найдена, попробуйте ещё раз:")
        return
    # Сохраняем в состоянии выбранную группу и устанавливаем параметры по умолчанию
    await state.update_data(group_name=group_name, group_id=group_obj.group_id, day_offset=0,
                            parity="Четная" if datetime.datetime.now().isocalendar()[1] % 2 == 0 else "Нечетная")
    await send_schedule(message.bot, message.chat.id, state)
    await state.set_state(ScheduleStates.schedule)


# Обработчик нажатий по inline-клавиатуре для навигации в расписании
@router.callback_query(lambda c: c.data and c.data.startswith("schedule:"))
async def process_schedule_callbacks(call: types.CallbackQuery, state: FSMContext):
    data_parts = call.data.split(":")
    data = await state.get_data()
    action = data_parts[1]
    if action == "prev":
        day_offset = data.get("day_offset", 0) - 1
        print(f"day_offset: {day_offset}")
        await state.update_data(day_offset=day_offset)
        parity = "Четная" if even_week(datetime.date.today() + datetime.timedelta(days=day_offset)) else "Нечетная"
        await state.update_data(parity=parity)
        await call.answer("Предыдущий день")
    elif action == "next":
        day_offset = data.get("day_offset", 0) + 1
        await state.update_data(day_offset=day_offset)
        parity = "Четная" if even_week(datetime.date.today() + datetime.timedelta(days=day_offset)) else "Нечетная"
        await state.update_data(parity=parity)
        await call.answer("Следующий день")
    elif action == "today":
        await state.update_data(day_offset=0)
        parity = "Четная" if even_week(datetime.date.today()) else "Нечетная"
        await state.update_data(parity=parity)
        await call.answer("Сегодня")
    elif action == "parity":
        # Переключаем тип недели на тот, что указали
        new_parity = data_parts[2]
        await state.update_data(parity=new_parity)
        await call.answer(f"Установлено: {new_parity}")
    elif action == "select_day":
        # Выбирается конкретный день недели (Пн, Вт, Ср, Чт, Пт)
        selected_day = data_parts[2]
        # Вычисляем смещение: определим текущий номер недели и смещение до выбранного дня
        days_order = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        target_index = days_order.index(selected_day) if selected_day in days_order else 0
        today_index = datetime.date.today().weekday()  # 0 = понедельник
        new_offset = target_index - today_index
        await state.update_data(day_offset=new_offset)
        await call.answer(f"Выбран: {selected_day}")
    # После изменения параметров удаляем старое сообщение и отправляем новое расписание
    chat_id = call.message.chat.id
    await call.message.delete()
    await send_schedule(call.bot, chat_id, state)
