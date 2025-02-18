from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_inline_kb(is_admin: bool = False):
    buttons = [
        [InlineKeyboardButton(text="Расписание внеучебных занятий", callback_data="enter_extracurricular_activities_menu"),
        
        ],
        [InlineKeyboardButton(text="Контакты", callback_data="enter_contacts_menu"),
        InlineKeyboardButton(text="Расписание мероприятий", callback_data="enter_events_menu"),],
        [
        InlineKeyboardButton(text="Обратная связь и предложения", callback_data="enter_feedback_and_suggestions_menu"),
        ]
    ]
    if is_admin:
        buttons.append([InlineKeyboardButton(text="Админ-панель", callback_data="enter_admin_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
