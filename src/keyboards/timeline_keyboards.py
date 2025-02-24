from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def timeline_menu_inline_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="На сегодня", callback_data="enter_today_menu")],
            [InlineKeyboardButton(text="На неделю", callback_data="enter_week_menu")],
            [InlineKeyboardButton(text="На месяц", callback_data="enter_month_menu")],
            # [InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")],
        ]
    )
