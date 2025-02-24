from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def mero_kb(week_offset: int):
    buttons = []
    buttons.append(InlineKeyboardButton(text="Предыдущая неделя", callback_data=f"events_week_{week_offset-1}"))
    buttons.append(InlineKeyboardButton(text="Следующая неделя", callback_data=f"events_week_{week_offset+1}"))
    buttons.append(InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

def categories_kb():
    buttons = []
    #@router.callback_query(F.data.in_({"enter_career_mero_menu", "enter_science_mero_menu", "enter_civic_mero_menu", "enter_cultural_mero_menu", "enter_sport_mero_menu", "enter_all_mero_menu"}))
    buttons.append(InlineKeyboardButton(text="Карьерные", callback_data="admin_mero_career"))
    buttons.append(InlineKeyboardButton(text="Научные", callback_data="admin_mero_science"))
    buttons.append(InlineKeyboardButton(text="Гражданско-патриотические", callback_data="admin_mero_civic"))
    buttons.append(InlineKeyboardButton(text="Культурно-массовые", callback_data="admin_mero_cultural"))    
    buttons.append(InlineKeyboardButton(text="Спортивные", callback_data="admin_mero_sport"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])