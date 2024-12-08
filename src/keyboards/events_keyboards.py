from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def events_kb(week_offset: int):
    buttons = []
    buttons.append(InlineKeyboardButton(text="Предыдущая неделя", callback_data=f"events_week_{week_offset-1}"))
    buttons.append(InlineKeyboardButton(text="Следующая неделя", callback_data=f"events_week_{week_offset+1}"))
    buttons.append(InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
