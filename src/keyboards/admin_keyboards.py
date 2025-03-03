from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_kb():
    # Кнопки в 3 столбца.
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить меро", callback_data="admin_add_mero"),
            InlineKeyboardButton(text="Удал. меро", callback_data="admin_delete_mero")
        ],
        [
            InlineKeyboardButton(text="Ред. сообщение внеучебных занятий", callback_data="admin_edit_extracurricular_activities_message")
        ],
        [
            InlineKeyboardButton(text="Все пользователи", callback_data="admin_users_page_0"),
            InlineKeyboardButton(text="Все меро", callback_data="admin_meros_page_0"),
            InlineKeyboardButton(text="Все предложения", callback_data="admin_suggestions_page_0"),
            InlineKeyboardButton(text="Вся обратная связь", callback_data="admin_feedback_page_0")
        ],
        [
            # InlineKeyboardButton(text="Упр. уведомл.", callback_data="admin_toggle_user_notifications"),
            InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")
        ]
    ])

def extracurricular_activities_admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Творческие секции, студии, клубы", callback_data="admin_edit_extracurricular_activities_message_tssk"),
            
        ],
        [InlineKeyboardButton(text="Спортивные секции и сборные команды", callback_data="admin_edit_extracurricular_activities_message_sssk")],
        [
            InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")
        ]
    ])