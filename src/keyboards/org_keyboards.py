from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def org_kb(page: int):
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f"org_prev_{page-1}"))
    navigation_buttons.append(InlineKeyboardButton(text="Далее", callback_data=f"org_next_{page+1}"))

    back_button = [InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")]

    return InlineKeyboardMarkup(inline_keyboard=[navigation_buttons, back_button])
