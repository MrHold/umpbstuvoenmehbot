from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_kb():
    # Кнопки в 3 столбца.
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить меро", callback_data="admin_add_mero"),
            InlineKeyboardButton(text="Ред. меро", callback_data="admin_edit_mero"),
            InlineKeyboardButton(text="Удал. меро", callback_data="admin_delete_mero")
        ],
        [
            InlineKeyboardButton(text="Добавить внеучебное занятие.", callback_data="admin_add_extracurricular_activities"),
            InlineKeyboardButton(text="Ред. внеучебное занятие", callback_data="admin_edit_extracurricular_activities"),
            InlineKeyboardButton(text="Удал. внеучебное занятие", callback_data="admin_delete_extracurricular_activities")
        ],
        [
            InlineKeyboardButton(text="Все пользователи", callback_data="admin_users_page_0"),
            InlineKeyboardButton(text="Все меро", callback_data="admin_meros_page_0"),
            InlineKeyboardButton(text="Все внеучебные занятия", callback_data="admin_extracurricular_activities_page_0")
        ],
        [
            # InlineKeyboardButton(text="Упр. уведомл.", callback_data="admin_toggle_user_notifications"),
            InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")
        ]
    ])
