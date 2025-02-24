from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def suggestions_menu_inline_kb():
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="enter_feedback_and_suggestions_menu"),],
        [InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")],        
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

