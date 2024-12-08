# Для примера, можно добавить кнопки добавления/редактирования мероприятий.
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_kb():
    # Кнопки в 3 столбца.
    # В нашем случае: Добавить/Редактировать/Удалить событие, Добавить/Редактировать/Удалить организацию, Управление уведомлениями
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить меро", callback_data="admin_add_event"),
            InlineKeyboardButton(text="Ред. меро", callback_data="admin_edit_event"),
            InlineKeyboardButton(text="Удал. меро", callback_data="admin_delete_event")
        ],
        [
            InlineKeyboardButton(text="Добавить орг.", callback_data="admin_add_org"),
            InlineKeyboardButton(text="Ред. орг.", callback_data="admin_edit_org"),
            InlineKeyboardButton(text="Удал. орг.", callback_data="admin_delete_org")
        ],
        [
            InlineKeyboardButton(text="Все пользователи", callback_data="admin_users_page_0"),
            InlineKeyboardButton(text="Все меро", callback_data="admin_events_page_0"),
            InlineKeyboardButton(text="Все орг.", callback_data="admin_orgs_page_0")
        ],
        [
            InlineKeyboardButton(text="Упр. уведомл.", callback_data="admin_toggle_user_notifications"),
            InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")
        ]
    ])
