from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def contacts_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Управление молодёжной политики и студенческого досуга", callback_data="umpvd_contacts")],
            [InlineKeyboardButton(text="Спортивный клуб «ВОЕНМЕХ»", callback_data="sk_voenmeh_contacts")],
            [InlineKeyboardButton(text="Центр проектной деятельности", callback_data="cpd_contacts")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]
        ]
    )

def back_to_contacts_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="enter_contacts_menu"),
             InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")]
        ]
    )
