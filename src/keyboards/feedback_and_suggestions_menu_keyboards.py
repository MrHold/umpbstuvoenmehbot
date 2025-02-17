from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def feedback_menu_inline_kb():
    buttons = []
    buttons.append(InlineKeyboardButton(text="Обратная связь", callback_data="enter_feedback_menu"))
    buttons.append(InlineKeyboardButton(text="Предложения", callback_data="enter_suggestions_menu"))
    buttons.append(InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
