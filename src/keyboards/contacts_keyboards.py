from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def contacts_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")]
        ]
    )
