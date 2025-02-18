from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def feedback_menu_inline_kb():
    buttons = [
        [InlineKeyboardButton(text="Обратная связь по мероприятию", callback_data="enter_org_menu"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
