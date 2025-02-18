from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from src.utils.config_loader import CONFIG
from src.db.sessions import get_db
from src.db.models.user import User
from db.models.extracurricular_event import ExtracurricularEvent
from sqlalchemy import select, delete
from src.db.models.organization import Organization
from datetime import datetime
from src.utils.notification_utils import notify_new_event
from src.keyboards.admin_keyboards import admin_kb

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from natasha import DatesExtractor, MorphVocab, Doc
from razdel import tokenize

router = Router()
morph_vocab = MorphVocab()

DEFAULT_LOCATION = "БГТУ «ВОЕНМЕХ» им. Д.Ф. Устинова"
ITEMS_PER_PAGE = 5

class AddEventStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_date_input = State()
    waiting_for_time_input = State()
    waiting_for_location_input = State()
    waiting_for_description = State()

class EditEventStates(StatesGroup):
    waiting_for_event_id = State()
    waiting_for_new_data = State()

class DeleteEventStates(StatesGroup):
    waiting_for_event_id = State()

class AddOrgStates(StatesGroup):
    waiting_for_org_name = State()
    waiting_for_org_description = State()
    waiting_for_org_contacts = State()
    waiting_for_org_direction = State()

class EditOrgStates(StatesGroup):
    waiting_for_org_id = State()
    waiting_for_new_org_data = State()

class DeleteOrgStates(StatesGroup):
    waiting_for_org_id = State()

class ToggleUserNotifications(StatesGroup):
    waiting_for_user_id = State()

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

@router.callback_query(F.data == "admin_add_event")
async def admin_add_event(call: types.CallbackQuery, state: FSMContext):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return
    await call.message.edit_text("Введите название мероприятия:")
    await state.set_state(AddEventStates.waiting_for_title)
    await call.answer()

@router.message(AddEventStates.waiting_for_title)
async def add_event_title(message: types.Message, state: FSMContext):
    title = message.text.strip()
    if not title:
        await message.answer("Название не может быть пустым. Попробуйте снова.")
        return
    await state.update_data(title=title)
    await message.answer("Введите дату мероприятия (например: '15 апреля 2025' или '01.01.2025'). Если не хотите указывать дату, отправьте 'нет'.")
    await state.set_state(AddEventStates.waiting_for_date_input)

@router.message(AddEventStates.waiting_for_date_input)
async def add_event_date(message: types.Message, state: FSMContext):
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
    await state.set_state(AddEventStates.waiting_for_time_input)

@router.message(AddEventStates.waiting_for_time_input)
async def add_event_time(message: types.Message, state: FSMContext):
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
    await state.set_state(AddEventStates.waiting_for_location_input)

@router.message(AddEventStates.waiting_for_location_input)
async def add_event_location(message: types.Message, state: FSMContext):
    location = message.text.strip()
    if location.lower() == "нет":
        location = DEFAULT_LOCATION
    await state.update_data(location=location)

    await message.answer("Введите описание мероприятия:")
    await state.set_state(AddEventStates.waiting_for_description)

@router.message(AddEventStates.waiting_for_description)
async def add_event_description(message: types.Message, state: FSMContext):
    description = message.text.strip()
    data = await state.get_data()
    title = data["title"]
    date = data.get("date", datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0))
    location = data["location"]

    async with get_db() as db:
        new_event = Event(
            title=title, 
            date=date,  # Может быть None если без даты
            location=location, 
            description=description, 
            is_active=True
        )
        db.add(new_event)
        await db.commit()
        await db.refresh(new_event)

    await message.answer("Мероприятие добавлено!")
    await state.clear()

    # Уведомляем подписчиков
    await notify_new_event(message.bot, new_event)

# ---------------------------- Редактирование мероприятия ----------------------------
@router.callback_query(F.data == "admin_edit_event")
async def admin_edit_event(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите ID мероприятия для редактирования:")
    await state.set_state(EditEventStates.waiting_for_event_id)
    await call.answer()

@router.message(EditEventStates.waiting_for_event_id)
async def edit_event_id(message: types.Message, state: FSMContext):
    try:
        event_id = int(message.text.strip())
    except ValueError:
        await message.answer("ID должен быть числом. Попробуйте снова.")
        return
    async with get_db() as db:
        result = await db.execute(select(Event).where(Event.id == event_id))
        ev = result.scalar()
        if not ev:
            await message.answer("Мероприятие не найдено.")
            await state.clear()
            return

    await state.update_data(event_id=event_id)
    await message.answer("Введите новые данные мероприятия в формате: Название|Дата(или 'нет')|Время(или 'нет')|Место(или 'нет')|Описание(или 'нет')\nЕсли не хотите менять поле — пишите 'нет'.")
    await state.set_state(EditEventStates.waiting_for_new_data)

@router.message(EditEventStates.waiting_for_new_data)
async def process_edit_event(message: types.Message, state: FSMContext):
    parts = message.text.split("|")
    while len(parts) < 5:
        parts.append("нет")

    new_title = parts[0].strip()
    new_date_str = parts[1].strip().lower()
    new_time_str = parts[2].strip().lower()
    new_location = parts[3].strip()
    new_description = parts[4].strip()

    data = await state.get_data()
    event_id = data["event_id"]

    async with get_db() as db:
        result = await db.execute(select(Event).where(Event.id == event_id))
        ev = result.scalar()
        if not ev:
            await message.answer("Мероприятие не найдено.")
            await state.clear()
            return

        # Обновление полей
        if new_title != "нет":
            ev.title = new_title

        if new_date_str != "нет":
            dates_extractor = DatesExtractor(morph_vocab)
            tokens = list(tokenize(new_date_str))
            doc_text = " ".join([_.text for _ in tokens])
            matches = [match.fact for match in dates_extractor(doc_text)]
            if matches:
                fact = matches[0]
                year = fact.year if fact.year else ev.date.year if ev.date else datetime.now().year
                month = fact.month if fact.month else ev.date.month if ev.date else datetime.now().month
                day = fact.day if fact.day else ev.date.day if ev.date else datetime.now().day
                new_date = datetime(year, month, day, 0, 0)
                ev.date = new_date
            else:
                # Если не поняли дату, оставим как было.
                pass
        else:
            # Если сказали "нет" дате, значит оставляем прежнее значение
            pass

        if new_time_str != "нет" and ev.date is not None:
            import re
            time_match = re.match(r'(\d{1,2}):(\d{2})', new_time_str)
            if time_match:
                hour, minute = int(time_match.group(1)), int(time_match.group(2))
                ev.date = ev.date.replace(hour=hour, minute=minute)
        # Если "нет", не меняем время
        # Если нет даты, время менять не актуально

        if new_location.lower() != "нет":
            ev.location = new_location

        if new_description.lower() != "нет":
            ev.description = new_description

        await db.commit()

    await message.answer("Мероприятие обновлено!")
    await state.clear()

# ---------------------------- Удаление мероприятия ----------------------------
@router.callback_query(F.data == "admin_delete_event")
async def admin_delete_event(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите ID мероприятия для удаления:")
    await state.set_state(DeleteEventStates.waiting_for_event_id)
    await call.answer()

@router.message(DeleteEventStates.waiting_for_event_id)
async def process_delete_event(message: types.Message, state: FSMContext):
    try:
        event_id = int(message.text.strip())
    except ValueError:
        await message.answer("ID должен быть числом.")
        return

    async with get_db() as db:
        await db.execute(delete(Event).where(Event.id == event_id))
        await db.commit()

    await message.answer("Мероприятие удалено.")
    await state.clear()

# ---------------------------- Добавление Организации ----------------------------
@router.callback_query(F.data == "admin_add_org")
async def admin_add_org(call: types.CallbackQuery, state: FSMContext):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return
    await call.message.edit_text("Введите название организации:")
    await state.set_state(AddOrgStates.waiting_for_org_name)
    await call.answer()

@router.message(AddOrgStates.waiting_for_org_name)
async def org_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Название не может быть пустым.")
        return
    await state.update_data(name=name)
    await message.answer("Введите описание или 'нет' для пропуска:")
    await state.set_state(AddOrgStates.waiting_for_org_description)

@router.message(AddOrgStates.waiting_for_org_description)
async def org_description(message: types.Message, state: FSMContext):
    desc = message.text.strip()
    if desc.lower() == "нет":
        desc = ""
    await state.update_data(description=desc)
    await message.answer("Введите контакты или 'нет' для пропуска:")
    await state.set_state(AddOrgStates.waiting_for_org_contacts)

@router.message(AddOrgStates.waiting_for_org_contacts)
async def org_contacts(message: types.Message, state: FSMContext):
    contacts = message.text.strip()
    if contacts.lower() == "нет":
        contacts = ""
    await state.update_data(contacts=contacts)
    await message.answer("Введите направление или 'нет' для пропуска:")
    await state.set_state(AddOrgStates.waiting_for_org_direction)

@router.message(AddOrgStates.waiting_for_org_direction)
async def org_direction(message: types.Message, state: FSMContext):
    direction = message.text.strip()
    if direction.lower() == "нет":
        direction = ""

    data = await state.get_data()
    name = data["name"]
    description = data["description"]
    contacts = data["contacts"]
    direction_ = direction

    async with get_db() as db:
        new_org = Organization(name=name, description=description, contacts=contacts, direction=direction_)
        db.add(new_org)
        await db.commit()
        await db.refresh(new_org)

    await message.answer("Организация добавлена!")
    await state.clear()

# ---------------------------- Редактирование Организации ----------------------------
@router.callback_query(F.data == "admin_edit_org")
async def admin_edit_org(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите ID организации для редактирования:")
    await state.set_state(EditOrgStates.waiting_for_org_id)
    await call.answer()

@router.message(EditOrgStates.waiting_for_org_id)
async def edit_org_id(message: types.Message, state: FSMContext):
    try:
        org_id = int(message.text.strip())
    except ValueError:
        await message.answer("ID должен быть числом.")
        return

    async with get_db() as db:
        result = await db.execute(select(Organization).where(Organization.id == org_id))
        org = result.scalar()
        if not org:
            await message.answer("Организация не найдена.")
            await state.clear()
            return

    await state.update_data(org_id=org_id)
    await message.answer("Введите новые данные организации в формате: Название|Описание(или 'нет')|Контакты(или 'нет')|Направление(или 'нет'). Если не хотите менять поле — пишите 'нет'.")
    await state.set_state(EditOrgStates.waiting_for_new_org_data)

@router.message(EditOrgStates.waiting_for_new_org_data)
async def process_edit_org(message: types.Message, state: FSMContext):
    parts = message.text.split("|")
    while len(parts) < 4:
        parts.append("нет")

    new_name = parts[0].strip()
    new_desc = parts[1].strip()
    new_contacts = parts[2].strip()
    new_direction = parts[3].strip()

    data = await state.get_data()
    org_id = data["org_id"]

    async with get_db() as db:
        result = await db.execute(select(Organization).where(Organization.id == org_id))
        org = result.scalar()
        if not org:
            await message.answer("Организация не найдена.")
            await state.clear()
            return

        if new_name.lower() != "нет":
            org.name = new_name
        if new_desc.lower() != "нет":
            org.description = new_desc
        if new_contacts.lower() != "нет":
            org.contacts = new_contacts
        if new_direction.lower() != "нет":
            org.direction = new_direction

        await db.commit()

    await message.answer("Организация обновлена!")
    await state.clear()

# ---------------------------- Удаление Организации ----------------------------
@router.callback_query(F.data == "admin_delete_org")
async def admin_delete_org(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите ID организации для удаления:")
    await state.set_state(DeleteOrgStates.waiting_for_org_id)
    await call.answer()

@router.message(DeleteOrgStates.waiting_for_org_id)
async def process_delete_org(message: types.Message, state: FSMContext):
    try:
        org_id = int(message.text.strip())
    except ValueError:
        await message.answer("ID должен быть числом.")
        return

    async with get_db() as db:
        await db.execute(delete(Organization).where(Organization.id == org_id))
        await db.commit()

    await message.answer("Организация удалена.")
    await state.clear()

# ---------------------------- Управление уведомлениями пользователя ----------------------------
@router.callback_query(F.data == "admin_toggle_user_notifications")
async def admin_toggle_user_notifications(call: types.CallbackQuery, state: FSMContext):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return
    await call.message.edit_text("Введите Telegram ID пользователя, у которого хотите включить/выключить уведомления:")
    await state.set_state(ToggleUserNotifications.waiting_for_user_id)
    await call.answer()

@router.message(ToggleUserNotifications.waiting_for_user_id)
async def process_toggle_user_notifications(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer("ID должен быть числом.")
        return

    async with get_db() as db:
        result = await db.execute(select(User).where(User.telegram_id == user_id))
        usr = result.scalar()
        if not usr:
            await message.answer("Пользователь не найден.")
            await state.clear()
            return
        usr.is_subscribed_for_events = not usr.is_subscribed_for_events
        await db.commit()

    await message.answer(f"У пользователя {user_id} переключен флаг уведомлений на {usr.is_subscribed_for_events}.")
    await state.clear()

# ---------------- Пагинация мероприятий ----------------
@router.callback_query(F.data.startswith("admin_events_page_"))
async def list_events_pagination(call: types.CallbackQuery):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return

    # Извлекаем номер страницы
    _, _, page_str = call.data.partition("admin_events_page_")
    page = int(page_str)

    async with get_db() as db:
        result = await db.execute(select(Event))
        events = result.scalars().all()

    total = len(events)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_events = events[start:end]

    if not page_events and page > 0:
        # Если страница пуста, вернемся на предыдущую, если возможно
        await call.answer("Пустая страница")
        return

    text = "Все мероприятия:\n"
    for ev in page_events:
        date_str = ev.date.strftime("%Y-%m-%d %H:%M") if ev.date else "Нет даты"
        text += f"ID: {ev.id}\nНазвание: {ev.title}\nДата: {date_str}\nМесто: {ev.location}\nОписание: {ev.description}\nАктивно: {ev.is_active}\n---\n"

    # Кнопки пагинации
    kb = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f"admin_events_page_{page-1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="Далее", callback_data=f"admin_events_page_{page+1}"))
    if nav_buttons:
        kb.append(nav_buttons)

    kb.append([InlineKeyboardButton(text="Назад в админку", callback_data="enter_admin_menu")])

    markup = InlineKeyboardMarkup(inline_keyboard=kb)

    await call.message.edit_text(text, reply_markup=markup)
    await call.answer()

# ---------------- Пагинация объединений ----------------
@router.callback_query(F.data.startswith("admin_orgs_page_"))
async def list_orgs_pagination(call: types.CallbackQuery):
    admins = CONFIG["ADMINS"]
    if call.from_user.id not in admins:
        await call.answer("Нет доступа.")
        return

    _, _, page_str = call.data.partition("admin_orgs_page_")
    page = int(page_str)

    async with get_db() as db:
        result = await db.execute(select(Organization))
        orgs = result.scalars().all()

    total = len(orgs)
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_orgs = orgs[start:end]

    if not page_orgs and page > 0:
        await call.answer("Пустая страница")
        return

    text = "Все объединения:\n"
    for org in page_orgs:
        text += f"ID: {org.id}\nНазвание: {org.name}\nОписание: {org.description}\nКонтакты: {org.contacts}\nНаправление: {org.direction}\n---\n"

    kb = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f"admin_orgs_page_{page-1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(text="Далее", callback_data=f"admin_orgs_page_{page+1}"))
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
        text += f"ID: {u.id}\nTelegram ID: {u.telegram_id}\nПодписан на уведомления: {u.is_subscribed_for_events}\nАдмин: {u.is_admin}\n---\n"

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