from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def mero_menu_inline_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Карьерные", callback_data="enter_career_mero_menu")],
            [InlineKeyboardButton(text="Научные", callback_data="enter_science_mero_menu")],
            [InlineKeyboardButton(text="Гражданско-патриотические", callback_data="enter_civic_mero_menu")],
            [InlineKeyboardButton(text="Культурно-массовые", callback_data="enter_cultural_mero_menu")],
            [InlineKeyboardButton(text="Спортивные", callback_data="enter_sport_mero_menu")],
            [InlineKeyboardButton(text="Все", callback_data="enter_all_mero_menu")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")],
        ]
    )
