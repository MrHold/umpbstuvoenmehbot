from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def suggestions_menu_inline_kb():
    buttons = [
        [InlineKeyboardButton(text="Расписание внеучебных занятий", callback_data="enter_org_menu"),
        
        ],
        [InlineKeyboardButton(text="Контакты", callback_data="enter_contacts_menu"),],
        [InlineKeyboardButton(text="Расписание мероприятий", callback_data="enter_events_menu"),],
        [
        InlineKeyboardButton(text="Обратная связь и предложения", callback_data="enter_feedback_menu"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

