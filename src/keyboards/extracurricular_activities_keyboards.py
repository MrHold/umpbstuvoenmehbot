from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def extracurricular_activities_menu_inline_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Творческие секции, студии, клубы", callback_data="enter_events_menu")],
            [InlineKeyboardButton(text="Спортивные секции и сборные команды", callback_data="enter_org_menu")],
            [InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")],
        ]
    )
