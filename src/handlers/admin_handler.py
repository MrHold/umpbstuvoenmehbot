from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from src.utils.config_loader import CONFIG
from src.db.sessions import get_db
from src.db.models.user import User
from db.models.extracurricular_event import ExtracurricularEvent
from sqlalchemy import select, delete, insert, update
from src.db.models.meros import Mero
from src.db.models.feedback import Feedback
from datetime import datetime
# from src.utils.notification_utils import notify_new_mero
from src.keyboards.admin_keyboards import admin_kb, extracurricular_activities_admin_kb
from src.keyboards.mero_keyboards import categories_kb

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from natasha import DatesExtractor, MorphVocab, Doc
from razdel import tokenize

router = Router()
morph_vocab = MorphVocab()

DEFAULT_LOCATION = "БГТУ «ВОЕНМЕХ» им. Д.Ф. Устинова"
ITEMS_PER_PAGE = 5

class AddMeroStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_date_input = State()
    waiting_for_time_input = State()
    waiting_for_location_input = State()
    waiting_for_description = State()
    waiting_for_category = State()

class EditMeroStates(StatesGroup):
    waiting_for_mero_id = State()
    waiting_for_new_data = State()

class DeleteMeroStates(StatesGroup):
    waiting_for_mero_id = State()

class EditExtracurricularActivitiesMessage(StatesGroup):
    waiting_for_new_message_tssk = State()
    waiting_for_new_message_sssk = State()


@router.message(F.text == "Админ-панель")
async def admin_menu(message: types.Message):
    admins = CONFIG["ADMINS"]
    if message.from_user.id in admins:
        await message.answer("Админ-панель:", reply_markup=admin_kb())
    else:
        await message.answer("У вас нет прав доступа")

@router.callback_query(F.data == "enter_admin_menu")
async def enter_admin_menu(call: types.CallbackQuery):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.message.answer("Нет доступа.")
        await call.answer()
        return
    await call.message.edit_text("Админ-панель:", reply_markup=admin_kb())
    await call.answer()

@router.callback_query(F.data == "admin_add_mero")
async def admin_add_mero(call: types.CallbackQuery, state: FSMContext):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return
    await call.message.edit_text("Введите название мероприятия:")
    await state.set_state(AddMeroStates.waiting_for_title)
    await call.answer()

@router.message(AddMeroStates.waiting_for_title)
async def add_mero_title(message: types.Message, state: FSMContext):
    title = message.text.strip()
    if not title:
        await message.answer("Название не может быть пустым. Попробуйте снова.")
        return
    await state.update_data(title=title)
    await message.answer("Введите дату мероприятия (например: '15 апреля 2025' или '01.01.2025'). Если не хотите указывать дату, отправьте 'нет'.")
    await state.set_state(AddMeroStates.waiting_for_date_input)

@router.message(AddMeroStates.waiting_for_date_input)
async def add_mero_date(message: types.Message, state: FSMContext):
    text = message.text.strip().lower()
    if text == "нет":
        # Пользователь не хочет дату
        await state.update_data(date=datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0))
        # Если даты нет, время спрашивать бессмысленно, сразу спрашиваем место
        await ask_for_location(message, state)
        return

    dates_extractor = DatesExtractor(morph_vocab)
    tokens = list(tokenize(text))
    doc_text = " ".join([_.text for _ in tokens])
    matches = [match.fact for match in dates_extractor(doc_text)]
    if not matches:
        await message.answer("Не удалось понять дату. Отправьте 'нет', если не хотите указывать дату, или введите дату ещё раз.")
        return

    # Берём первую распознанную дату
    date = matches[0]
    year = date.year if date.year else datetime.now().year
    month = date.month if date.month else datetime.now().month
    day = date.day if date.day else datetime.now().day

    # Ставим время по умолчанию 00:00, потом спросим у пользователя отдельно
    date = datetime(year, month, day, 0, 0)
    await state.update_data(date=date)

    await message.answer("Введите время в формате 'HH:MM', или отправьте 'нет', если мероприятие без точного времени.")
    await state.set_state(AddMeroStates.waiting_for_time_input)

@router.message(AddMeroStates.waiting_for_time_input)
async def add_mero_time(message: types.Message, state: FSMContext):
    text = message.text.strip().lower()
    data = await state.get_data()
    date = data["date"]  # Может быть уже установленной датой или None

    if text == "нет":
        # Без времени - оставляем время 00:00, если дата была
        # Если даты нет - вообще не трогаем
        if date is not None:
            # date уже есть, оставляем как есть (00:00)
            pass
        await ask_for_location(message, state)
        return

    # Парсим время
    import re
    time_match = re.match(r'(\d{1,2}):(\d{2})', text)
    if not time_match:
        await message.answer("Неверный формат времени. Введите в формате HH:MM или 'нет' для пропуска.")
        return
    hour, minute = int(time_match.group(1)), int(time_match.group(2))
    if date is not None:
        # Обновляем дату с указанным временем
        date = date.replace(hour=hour, minute=minute)
        await state.update_data(date=date)
    # Если date=None (нет даты), то это не имеет смысла, но раз мы сюда дошли, дата не None

    await ask_for_location(message, state)

async def ask_for_location(message: types.Message, state: FSMContext):
    await message.answer("Введите место проведения мероприятия или отправьте 'нет' для использования места по умолчанию.")
    await state.set_state(AddMeroStates.waiting_for_location_input)

@router.message(AddMeroStates.waiting_for_location_input)
async def add_mero_location(message: types.Message, state: FSMContext):
    location = message.text.strip()
    if location.lower() == "нет":
        location = DEFAULT_LOCATION
    await state.update_data(location=location)

    await message.answer("Введите категорию мероприятия:", reply_markup=categories_kb())
    await state.set_state(AddMeroStates.waiting_for_category)

@router.callback_query(F.data.in_({"admin_mero_career", "admin_mero_science", "admin_mero_civic", "admin_mero_cultural", "admin_mero_sport"}))
async def add_mero_category(call: types.CallbackQuery, state: FSMContext):
    category = call.data.split("_")[-1]
    await state.update_data(category=category)
    await call.answer()
    await call.message.edit_text("Введите описание мероприятия:")
    await state.set_state(AddMeroStates.waiting_for_description)

@router.message(AddMeroStates.waiting_for_description)
async def add_mero_description(message: types.Message, state: FSMContext):
    description = message.text.strip()
    data = await state.get_data()
    title = data["title"]
    date = data.get("date", datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0))
    location = data["location"]
    category = data.get("category", "unknown")

    async with get_db() as db:
        new_mero = Mero(
            title=title, 
            date=date,  # Может быть None если без даты
            location=location, 
            description=description, 
            is_active=True,
            category=category
        )
        db.add(new_mero)
        await db.commit()
        await db.refresh(new_mero)

    await message.answer("Мероприятие добавлено!")
    await message.answer(f"ID: {new_mero.id}\nНазвание: {new_mero.title}\nДата: {new_mero.date}\nМесто: {new_mero.location}\nОписание: {new_mero.description}\nКатегория: {new_mero.category}")
    await message.answer("Админ-панель:", reply_markup=admin_kb())
    await state.clear()

    # Уведомляем подписчиков
    # await notify_new_mero(message.bot, new_mero)

# ---------------------------- Удаление мероприятия ----------------------------
@router.callback_query(F.data == "admin_delete_mero")
async def admin_delete_mero(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите ID мероприятия для удаления:")
    await state.set_state(DeleteMeroStates.waiting_for_mero_id)
    await call.answer()

@router.message(DeleteMeroStates.waiting_for_mero_id)
async def process_delete_mero(message: types.Message, state: FSMContext):
    try:
        mero_id = int(message.text.strip())
    except ValueError:
        await message.answer("ID должен быть числом.")
        return

    async with get_db() as db:
        await db.execute(delete(Mero).where(Mero.id == mero_id))
        await db.commit()

    await message.answer("Мероприятие удалено.")
    await message.answer("Админ-панель:", reply_markup=admin_kb())
    await state.clear()


# ---------------- Пагинация мероприятий ----------------
@router.callback_query(F.data.startswith("admin_meros_page_"))
async def list_mero_pagination(call: types.CallbackQuery):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return

    # Извлекаем номер страницы
    _, _, page_str = call.data.partition("admin_meros_page_")
    page = int(page_str)

    async with get_db() as db:
        result = await db.execute(select(Mero))
        mero = result.scalars().all()

    total = len(mero)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_meros = mero[start:end]

    if not page_meros and page > 0:
        # Если страница пуста, вернемся на предыдущую, если возможно
        await call.answer("Пустая страница")
        return

    text = "Все мероприятия:\n"
    for ev in page_meros:
        date_str = ev.date.strftime("%Y-%m-%d %H:%M") if ev.date else "Нет даты"
        text += f"ID: {ev.id}\nНазвание: {ev.title}\nДата: {date_str}\nМесто: {ev.location}\nОписание: {ev.description}\nАктивно: {ev.is_active}\nКатегория: {ev.category}\n---\n"

    # Кнопки пагинации
    kb = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f"admin_meros_page_{page-1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="Далее", callback_data=f"admin_meros_page_{page+1}"))
    if nav_buttons:
        kb.append(nav_buttons)

    kb.append([InlineKeyboardButton(text="Назад в админку", callback_data="enter_admin_menu")])

    markup = InlineKeyboardMarkup(inline_keyboard=kb)

    await call.message.edit_text(text, reply_markup=markup)
    await call.answer()


# ---------------- Пагинация пользователей ----------------
@router.callback_query(F.data.startswith("admin_users_page_"))
async def list_users_pagination(call: types.CallbackQuery):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return

    _, _, page_str = call.data.partition("admin_users_page_")
    page = int(page_str)

    async with get_db() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()

    total = len(users)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_users = users[start:end]

    if not page_users and page > 0:
        await call.answer("Пустая страница")
        return

    text = "Все пользователи:\n"
    for u in page_users:
        text += f"ID: {u.id}\nTelegram ID: {u.telegram_id}\nUsername: {u.username}\nName: {u.name}\nАдмин: {u.is_admin}\n---\n"

    kb = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f"admin_users_page_{page-1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="Далее", callback_data=f"admin_users_page_{page+1}"))
    if nav_buttons:
        kb.append(nav_buttons)

    kb.append([InlineKeyboardButton(text="Назад в админку", callback_data="enter_admin_menu")])

    markup = InlineKeyboardMarkup(inline_keyboard=kb)

    await call.message.edit_text(text, reply_markup=markup)
    await call.answer()
#admin_edit_extracurricular_activities_message
@router.callback_query(F.data == "admin_edit_extracurricular_activities_message")
async def admin_edit_extracurricular_activities_message(call: types.CallbackQuery, state: FSMContext):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return
    await call.message.edit_text("Выберите сообщение: ", reply_markup=extracurricular_activities_admin_kb())
    await call.answer()
    # await state.set_state(EditExtracurricularActivitiesMessage.waiting_for_new_message)

@router.callback_query(F.data == "admin_edit_extracurricular_activities_message_tssk")
async def admin_edit_extracurricular_activities_message_tssk(call: types.CallbackQuery, state: FSMContext):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return
    kb = []
    kb.append([InlineKeyboardButton(text="Назад в админку", callback_data="enter_admin_menu")])
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await call.message.edit_text("Введите новое сообщение для мероприятий: ", reply_markup=markup)
    await call.answer()
    await state.set_state(EditExtracurricularActivitiesMessage.waiting_for_new_message_tssk)

@router.callback_query(F.data == "admin_edit_extracurricular_activities_message_sssk")
async def admin_edit_extracurricular_activities_message_tssk(call: types.CallbackQuery, state: FSMContext):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return
    kb = []
    kb.append([InlineKeyboardButton(text="Назад в админку", callback_data="enter_admin_menu")])
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await call.message.edit_text("Введите новое сообщение для мероприятий: ", reply_markup=markup)
    await call.answer()
    await state.set_state(EditExtracurricularActivitiesMessage.waiting_for_new_message_sssk)

@router.message(EditExtracurricularActivitiesMessage.waiting_for_new_message_tssk)
async def save_new_message_tssk(message: types.Message, state: FSMContext):
    admins = CONFIG["ADMINS"]
    if message.from_user.id not in admins:
        await message.answer("Нет доступа.")
        return
        
    new_message = message.text
    async with get_db() as db:
        # Check if record exists
        result = await db.execute(
            select(ExtracurricularEvent).where(ExtracurricularEvent.id == 1)
        )
        existing_record = result.scalar_one_or_none()
        
        if not existing_record:
            # Create new record
            new_event = ExtracurricularEvent(
                id=1,
                message=new_message
            )
            db.add(new_event)
        else:
            # Update existing record
            existing_record.message = new_message
            
        await db.commit()
        
    await message.answer("Сообщение успешно обновлено.", reply_markup=admin_kb())
    await state.clear()

@router.message(EditExtracurricularActivitiesMessage.waiting_for_new_message_sssk)
async def save_new_message_sssk(message: types.Message, state: FSMContext):
    admins = CONFIG["ADMINS"]
    if message.from_user.id not in admins:
        await message.answer("Нет доступа.")
        return
        
    new_message = message.text
    async with get_db() as db:
        # Check if record exists
        result = await db.execute(
            select(ExtracurricularEvent).where(ExtracurricularEvent.id == 2)
        )
        existing_record = result.scalar_one_or_none()
        
        if not existing_record:
            # Create new record
            new_event = ExtracurricularEvent(
                id=2,
                message=new_message
            )
            db.add(new_event)
        else:
            # Update existing record
            existing_record.message = new_message
            
        await db.commit()
        
    await message.answer("Сообщение успешно обновлено.", reply_markup=admin_kb())
    await state.clear()

@router.callback_query(F.data.startswith("admin_suggestions_page_"))
async def list_suggestions_pagination(call: types.CallbackQuery):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return

    _, _, page_str = call.data.partition("admin_suggestions_page_")
    page = int(page_str)

    async with get_db() as db:
        result = await db.execute(select(Feedback).where(Feedback.type == "suggestion"))
        suggestions = result.scalars().all()

    total = len(suggestions)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_suggestions = suggestions[start:end]

    if not page_suggestions and page > 0:
        await call.answer("Пустая страница")
        return

    text = "Все предложения:\n"
    for s in page_suggestions:
        text += f"ID: {s.id}\nTelegram ID: {s.telegram_id}\nUsername: {s.username}\nName: {s.name}\nСообщение: {s.message}\nКонтакты: {s.contact}\n---\n"

    kb = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f"admin_suggestions_page_{page-1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="Далее", callback_data=f"admin_suggestions_page_{page+1}"))
    if nav_buttons:
        kb.append(nav_buttons)

    kb.append([InlineKeyboardButton(text="Назад в админку", callback_data="enter_admin_menu")])

    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await call.message.edit_text(text, reply_markup=markup, disable_web_page_preview=True, link_preview_options={"is_disabled": True})
    # if len(text) > 4096:
    #     while len(text) > 4096:
    #         end = min(len(text), 4096)
    #         temptext = text[:end]
    #         await call.message.answer(temptext, reply_markup=markup, disable_web_page_preview=True, link_preview_options={"is_disabled": True})
    #         text = temptext
    #     if text:
    #         await call.message.answer(text, reply_markup=markup, disable_web_page_preview=True, link_preview_options={"is_disabled": True})
    # else:
    #     await call.message.edit_text(text, reply_markup=markup, disable_web_page_preview=True, link_preview_options={"is_disabled": True})

    await call.answer()

@router.callback_query(F.data.startswith("admin_feedback_page_"))
async def list_feedback_pagination(call: types.CallbackQuery):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return

    _, _, page_str = call.data.partition("admin_feedback_page_")
    page = int(page_str)

    async with get_db() as db:
        result = await db.execute(select(Feedback).where(Feedback.type == "feedback"))
        feedbacks = result.scalars().all()

    total = len(feedbacks)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_feedbacks = feedbacks[start:end]

    if not page_feedbacks and page > 0:
        await call.answer("Пустая страница")
        return

    text = "Все обратная связь:\n"
    for f in page_feedbacks:
        text += f"ID: {f.id}\nTelegram ID: {f.telegram_id}\nUsername: {f.username}\nName: {f.name}\nСообщение: {f.message}\n\n---\n"

    kb = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f"admin_feedback_page_{page-1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="Далее", callback_data=f"admin_feedback_page_{page+1}"))
    if nav_buttons:
        kb.append(nav_buttons)
    # text += str(total)
    kb.append([InlineKeyboardButton(text="Назад в админку", callback_data="enter_admin_menu")])
    lentext = len(text)
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await call.message.edit_text(text, reply_markup=markup, disable_web_page_preview=True, link_preview_options={"is_disabled": True})
    # if len(text) > 4096:
    #     while len(text) > 4096:
    #         end = min(len(text), 4096)
    #         temptext = text[:end]
    #         await call.message.answer(temptext, reply_markup=markup, disable_web_page_preview=True, link_preview_options={"is_disabled": True})
    #         text = temptext
    #     if text:
    #         await call.message.answer(text, reply_markup=markup, disable_web_page_preview=True, link_preview_options={"is_disabled": True})
    # else:
        # await call.message.edit_text(text, reply_markup=markup, disable_web_page_preview=True, link_preview_options={"is_disabled": True})
    await call.answer()

