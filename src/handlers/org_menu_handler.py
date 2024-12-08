from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from src.keyboards.org_keyboards import org_kb
from src.db.sessions import get_db
from src.db.models.organization import Organization
from sqlalchemy.future import select

router = Router()

class OrgStates(StatesGroup):
    page = State()

@router.callback_query(F.data == "enter_org_menu")
async def show_organizations_list(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(OrgStates.page)
    await state.update_data(page=0)
    text = await get_org_list_text(0)
    # Отправляем новое сообщение (так как это первый заход в меню)
    new_message = await call.message.edit_text(text, reply_markup=org_kb(0))
    await call.answer()  # отвечаем на callback, убираем "часики"

@router.callback_query(F.data.startswith("org_"))
async def org_pagination(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")  # формат: org_next_1 или org_prev_0
    # data[0] = "org"
    # data[1] = "next" или "prev"
    # data[2] = новая страница (число)

    direction = data[1]
    new_page = int(data[2])

    # Получаем текущую страницу из состояния
    current_data = await state.get_data()
    old_page = current_data.get("page", 0)

    # Если страница не изменилась (например, попытка уйти назад с 0-й страницы)
    if new_page == old_page:
        await call.answer("Страница не изменена")
        return

    # Обновляем страницу в состоянии
    await state.update_data(page=new_page)

    text = await get_org_list_text(new_page)
    await call.message.edit_text(text, reply_markup=org_kb(new_page))
    await call.answer()

async def get_org_list_text(page: int) -> str:
    limit = 10
    offset = page * limit
    async with get_db() as db:
        result = await db.execute(select(Organization).limit(limit).offset(offset))
        organizations = result.scalars().all()

    if not organizations:
        return "Нет данных или страница пуста."

    text = "Список объединений:\n"
    for org in organizations:
        text += f"- {org.name}\n{org.description}\n{org.contacts}\n{org.direction}\n\n"
    return text
