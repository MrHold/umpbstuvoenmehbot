from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_inline_kb(is_admin: bool = False):
    buttons = [
        [InlineKeyboardButton(text="Объединения", callback_data="enter_org_menu"),
        InlineKeyboardButton(text="Мероприятия", callback_data="enter_events_menu"),
        InlineKeyboardButton(text="Уведомления", callback_data="enter_subs_menu")],
        # [InlineKeyboardButton(text="Контакты/Информация", callback_data="enter_contacts_menu")],
    ]
    if is_admin:
        buttons.append([InlineKeyboardButton(text="Админ-панель", callback_data="enter_admin_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
