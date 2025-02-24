from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def contacts_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Управление молодёжной политики и студенческого досуга", callback_data="back_to_main_menu")],
            [InlineKeyboardButton(text="Спортивный клуб «ВОЕНМЕХ»", callback_data="back_to_main_menu")],
            [InlineKeyboardButton(text="Центр проектной деятельности", callback_data="back_to_main_menu")],
            [InlineKeyboardButton(text="Назад", callback_data="enter_contacts_menu")]
        ]
    )
