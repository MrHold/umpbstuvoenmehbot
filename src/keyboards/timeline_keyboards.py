from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def timeline_menu_inline_kb(category: str = "all") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="На сегодня", callback_data=f"enter_today_menu_{category}")],
            [InlineKeyboardButton(text="На неделю", callback_data=f"enter_week_menu_{category}")],
            [InlineKeyboardButton(text="На месяц", callback_data=f"enter_month_menu_{category}")],
            [InlineKeyboardButton(text="Назад", callback_data=f"enter_mero_menu")],
            [InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")],
        ]
    )

def back_to_timeline_menu_inline_kb(category: str = "all") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data=f"enter_{category}_mero_menu")],
            [InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")],
        ]
    )